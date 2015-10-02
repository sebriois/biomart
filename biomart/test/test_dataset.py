import unittest
import biomart
from biomart.lib import PUBLIC_BIOMART_URL


class BiomartDatasetTestCase(unittest.TestCase):
    def setUp(self):
        self.dataset = biomart.BiomartDataset(PUBLIC_BIOMART_URL, name="uniprot", verbose=True)

    def testCanConnectToDataset(self):
        self.assertTrue(self.dataset.server.is_alive)

    def testCanFetchFilters(self):
        self.dataset.fetch_filters()
        self.dataset.show_filters()
        self.assertTrue(len(self.dataset.filters.keys()) > 0)

    def testCanFetchAttributes(self):
        self.dataset.fetch_attributes()
        self.dataset.show_attributes()
        self.assertTrue(len(self.dataset.attributes.keys()) > 0)

    def testCanSearchWithMultipleFilters(self):
        response = self.dataset.search({
            'filters': {'accession': ['Q9FMA1', 'Q8LFJ9']}
        })
        rows = [line for line in response.iter_lines()]
        self.assertTrue(len(rows) > 0)
        self.assertFalse('Exception' in rows[0].decode('utf-8'))
    

def suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTest(loader.loadTestsFromTestCase(BiomartDatasetTestCase))
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
