import unittest, json, pathlib, importlib.util
ROOT=pathlib.Path(__file__).resolve().parents[2]
LIB=ROOT/'docs'/'scientific-evidence'
class ResearchLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.items=json.loads((LIB/'catalog.json').read_text(encoding='utf-8'))
    def test_more_than_one_hundred(self):self.assertGreater(len(self.items),100)
    def test_unique_files(self):self.assertEqual(len(self.items),len({r['file'] for r in self.items}))
    def test_sources_exist(self):self.assertTrue(all((LIB/r['file']).is_file() for r in self.items))
    def test_multilingual(self):self.assertTrue({'EN','ES','PT','FR','DE'}.issubset({r['lang'] for r in self.items}))
    def test_all_core_domains(self):
        have={r['domain'] for r in self.items}
        self.assertTrue({'solver','sciml','graph','marl','ledger','market','sdd','security'}.issubset(have))
    def test_no_fulltext_claims(self):
        self.assertTrue(all('full_text_reviewed: false' in (LIB/r['file']).read_text(encoding='utf-8') for r in self.items))
if __name__=='__main__':unittest.main()
