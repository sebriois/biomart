import unittest
import biomart
import os

class BiomartServerTestCase(unittest.TestCase):
    def setUp(self):
        self.server = biomart.BiomartServer() # url defaults to biomart.PUBLIC_BIOMART_URL

    def testCanConnect(self):
        self.assertTrue( self.server.is_alive )
    
    def testHasMartservice(self):
        self.assertTrue( '/martservice' in self.server.url )
    
    def testCanFetchDatabases(self):
        self.server.fetch_databases()
        self.assertTrue( len(self.server.databases.keys()) > 0 )

    def testCanFetchDatasets(self):
        self.server.fetch_datasets()
        self.assertTrue( len(self.server.datasets.keys()) > 0 )

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BiomartServerTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
