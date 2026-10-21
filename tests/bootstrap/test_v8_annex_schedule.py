import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
class TestPideAnnexSchedule(unittest.TestCase):
    def test_official_annex_structure_exists(self):
        doc=(ROOT/'docs/regulatory/PIDE-ANNEX-B1.2-PROCEDURE.md').read_text(encoding='utf-8')
        self.assertIn('procedimiento',doc.lower())
        self.assertIn('FONAFE',doc)
        self.assertIn('reconsideración',doc.lower())
        self.assertIn('a–p',doc)
    def test_source_unique_and_status(self):
        src=json.loads((ROOT/'docs/regulatory/SOURCES.json').read_text(encoding='utf-8'))
        ids=[x['id'] for x in src]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertIn('R080',ids)
        self.assertIn('MINEM_GDP2023',ids)
        self.assertIn('UNI_EU',ids)
if __name__=='__main__':unittest.main()
