"""V5 bootstrap tests. They validate contracts and small safe reference helpers, not systems."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load_package(package, filename, modname):
    path=ROOT/'packages/python'/package/'src'/modname/filename
    spec=importlib.util.spec_from_file_location(modname+'_'+filename.replace('.','_'),path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

G=load_package('power-graph','invariants.py','unitesis_graph')
L=load_package('power-ledger','attest.py','unitesis_ledger')
M=load_package('power-market','gates.py','unitesis_market')

class V5Tests(unittest.TestCase):
    def test_four_schemas_are_versioned_and_loadable(self):
        for name in ('graph-projection','p2p-envelope','p2p-energy-trade','ledger-anchor'):
            p=ROOT/'contracts/schemas/json'/f'{name}.v1.schema.json'
            d=json.loads(p.read_text(encoding='utf-8'))
            self.assertEqual(d['$schema'],'https://json-schema.org/draft/2020-12/schema')
            self.assertIn('schema_version',d['required'])
            self.assertFalse(d['additionalProperties'])
    def test_speckit_artifacts_per_feature(self):
        for ident in ('010-electrical-graph','011-p2p-federation','012-ledger-evidence','013-p2p-energy-market','014-graphrag-knowledge'):
            for f in ('spec.md','plan.md','tasks.md'):
                self.assertTrue((ROOT/'specs'/ident/f).is_file())
    def test_graph_rejects_invalid_edges_phases_and_snapshot(self):
        good={'network_snapshot_id':'s1','topology_hash':'f'*64,
              'nodes':[{'id':'a','phases':['A','B']},{'id':'b','phases':['A']}],
              'edges':[{'id':'e1','from_node':'a','to_node':'b','phase':'A','equipment_id':'line'}]}
        G.validate_projection(good)
        missing=copy.deepcopy(good);missing['edges'][0]['to_node']='orphan'
        with self.assertRaises(G.GraphProjectionError):G.validate_projection(missing)
        wrong=copy.deepcopy(good);wrong['edges'][0]['phase']='B'
        with self.assertRaises(G.GraphProjectionError):G.validate_projection(wrong)
        no_snapshot=copy.deepcopy(good);no_snapshot.pop('network_snapshot_id')
        with self.assertRaises(G.GraphProjectionError):G.validate_projection(no_snapshot)
    def test_digest_repeatable_and_modified_evidence_detected(self):
        orig={'z':2,'a':{'val':[1,2]}}
        h=L.digest_evidence(orig)
        self.assertEqual(h,L.digest_evidence({'a':{'val':[1,2]},'z':2}))
        self.assertTrue(L.matches_digest(orig,h))
        self.assertFalse(L.matches_digest({'z':2,'a':{'val':[2,1]}},h))
    def test_market_gate_fails_closed(self):
        proposed={'mode':'simulation','network_feasible':True}
        with self.assertRaises(M.MarketGateError):M.require_market_gates(proposed)
        authorized={'mode':'authorized-pilot','network_feasible':True,
            **{x:'evidence-id' for x in ('legal_approval_id','regulator_or_operator_approval_id',
                'metering_evidence_id','power_flow_evidence_id','network_snapshot_id','human_approval_id')}}
        M.require_market_gates(authorized)
        invalid=copy.deepcopy(authorized);invalid['network_feasible']=False
        with self.assertRaises(M.MarketGateError):M.require_market_gates(invalid)
        invalid=copy.deepcopy(authorized);invalid.pop('legal_approval_id')
        with self.assertRaises(M.MarketGateError):M.require_market_gates(invalid)

if __name__=='__main__':unittest.main()
