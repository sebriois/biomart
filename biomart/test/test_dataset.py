import unittest
import biomart
import os
import requests
from biomart.lib import PUBLIC_BIOMART_URL

class BiomartDatasetTestCase(unittest.TestCase):
    def setUp(self):
        self.dataset = biomart.BiomartDataset( url = PUBLIC_BIOMART_URL, name = 'uniprot' )
    
    def testCanConnectToDataset(self):
        self.assertTrue( self.dataset.is_alive )
    
    def testCanFetchConfiguration(self):
        self.dataset.fetch_configuration()
        self.assertTrue( len(self.dataset.filters.keys()) > 0 and len(self.dataset.attributes.keys()) > 0 )
    
    def testCanSearchWithDefaultAttributes(self):
        response = self.dataset.search({
            'filters': { 'accession': 'Q9MY58' }
        })
        self.assertTrue( response.status_code == requests.codes.ok )
    
    def testCanSearchWithMultipleFilters(self):
        response = self.dataset.search({
            'filters': { 'accession': ['Q9MY58','Q9URL2','Q9HGK6'] }
        })
        rows = [line for line in response.iter_lines()]
        self.assertTrue( len(rows) == 3 )
    

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BiomartDatasetTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
