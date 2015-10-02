import unittest
import biomart


class BiomartServerTestCase(unittest.TestCase):
    def setUp(self):
        self.server = biomart.BiomartServer(verbose=True)  # url defaults to biomart.PUBLIC_BIOMART_URL

    def testCanConnect(self):
        self.assertTrue(self.server.is_alive)
    
    def testHasMartservice(self):
        self.assertTrue('/martservice' in self.server.url)
    
    def testCanFetchAndShowDatabases(self):
        self.server.show_databases()
        self.assertTrue(len(self.server.databases.keys()) > 0)

    def testCanFetchAndShowDatasets(self):
        self.server.show_datasets()
        self.assertTrue(len(self.server.datasets.keys()) > 0)


def suite():
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTest(loader.loadTestsFromTestCase(BiomartServerTestCase))
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
