import importlib.util,json,unittest,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/python/power-regulation/src'))
from unitesis_regulation.pide_reference import assess_reference_case,annual_equivalent_cost,ReferenceGateError

class PIDEReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=json.loads((ROOT/'fixtures/pide/reference_case_synthetic.json').read_text(encoding='utf-8'))
    def payload(self):return json.loads(json.dumps(self.base))
    def test_historical_case_has_three_alternatives(self):
        self.assertTrue(assess_reference_case(self.payload())['documentary_complete'])
    def test_no_official_export(self):
        self.assertFalse(assess_reference_case(self.payload())['official_forms_export_allowed'])
    def test_no_original_annex_claim(self):
        self.assertFalse(assess_reference_case(self.payload())['original_minem_annex_verified'])
    def test_block_requested_certification(self):
        p=self.payload();p['request_official_certification']=True
        with self.assertRaises(ReferenceGateError):assess_reference_case(p)
    def test_block_spurious_regulatory_approval(self):
        p=self.payload();p['regulatory_label']='approved'
        with self.assertRaises(ReferenceGateError):assess_reference_case(p)
    def test_fewer_than_three_historical(self):
        p=self.payload();p['alternatives']=p['alternatives'][:2]
        self.assertFalse(assess_reference_case(p)['documentary_complete'])
    def test_other_company_has_no_three_default(self):
        p=self.payload();p['profile']='DISTRIBUTION_INTERNAL_STUDY';p['alternatives']=p['alternatives'][:2]
        self.assertTrue(assess_reference_case(p)['documentary_complete'])
    def test_explicit_rate_source_mandatory(self):
        p=self.payload();p.pop('discount_rate_source')
        self.assertFalse(assess_reference_case(p)['documentary_complete'])
    def test_solver_evidence_when_feasible(self):
        p=self.payload();p['alternatives'][0]['technical_feasibility']='feasible'
        self.assertFalse(assess_reference_case(p)['documentary_complete'])
    def test_negative_cost_blocked(self):
        with self.assertRaises(ReferenceGateError):annual_equivalent_cost(-1,0,0,0.1,30)
    def test_zero_rate_annuity(self):
        self.assertAlmostEqual(annual_equivalent_cost(100,1,2,0,10).equivalent_annual_cost,13)
    def test_format_registry_all_inactive(self):
        x=json.loads((ROOT/'config/regulations/pide_formats_original_pending.json').read_text(encoding='utf-8'))
        self.assertEqual(len(x['formats']),15)
        self.assertTrue(all(f['fields'] is None and f['official_export'] is False for f in x['formats']))
    def test_source_not_fabricated(self):
        src=json.loads((ROOT/'docs/regulatory/pide_2017/sources.json').read_text(encoding='utf-8'))
        self.assertFalse(src['annex_original_downloaded']);self.assertIsNone(src['annex_original_sha256'])
if __name__=='__main__':unittest.main()
