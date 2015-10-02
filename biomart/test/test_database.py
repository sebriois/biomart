import os
import unittest
from pprint import pprint

import biomart
from biomart.lib import PUBLIC_BIOMART_URL

class BiomartDatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.database = biomart.BiomartDatabase(PUBLIC_BIOMART_URL, name = 'unimart', verbose=True)
    
    def testCanConnectToDatabase(self):
        self.assertTrue( self.database.server.is_alive )
    
    def testCanFetchDatasets(self):
        self.database.fetch_datasets()
        self.assertTrue( len(self.database.datasets.keys()) > 0 )
    
    def testCanSelectDataset(self):
        uniprot = self.database.datasets['uniprot']
        self.assertTrue(uniprot.count() > 0)

def suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTest(loader.loadTestsFromTestCase(BiomartDatabaseTestCase))
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
