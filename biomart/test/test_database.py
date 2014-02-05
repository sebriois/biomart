import unittest
import biomart
import os

class BiomartDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.database = biomart.BiomartDatabase( url = biomart.TEST_URL, params = { 'name': 'unimart' })
        self.database.http_proxy = os.environ.get('http_proxy', None)
        
    def testCanConnectToDatabase(self):
        self.assertTrue( self.database.is_alive() )
    
    def testCanFetchDatasets(self):
        self.database.fetch_datasets()
        self.assertTrue( len(self.database.datasets.keys()) > 0 )
    
    def testCanSelectDataset(self):
        uniprot = self.database.datasets['uniprot']
        self.assertTrue( uniprot.is_alive() )
    

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BiomartDatabaseTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
