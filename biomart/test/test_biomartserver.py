import unittest
from biomart import BiomartServer

class BiomartTests(unittest.TestCase):
    def setUp(self):
        self.server = BiomartServer( url = "http://www.biomart.org/biomart" )
    
    def testIsAlive(self):
        self.assertTrue( self.server.is_alive() )
    
    def testHasBiomartService(self):
        self.assertTrue( '/martservice' in self.server.url )

def main():
    unittest.main()

if __name__ == '__main__':
    main()