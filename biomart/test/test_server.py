import unittest
import biomart
import os

class BiomartServerTestCase(unittest.TestCase):
    def setUp(self):
        self.server = biomart.BiomartServer( url = biomart.TEST_URL )
        self.server.http_proxy = os.environ.get('http_proxy', None)
    
    def testCanConnect(self):
        self.assertTrue( self.server.is_alive() )
    
    def testHasMartservice(self):
        self.assertTrue( '/martservice' in self.server.url )
    
    def testCanFetchDatabases(self):
        self.server.fetch_databases()
        self.assertTrue( len(self.server.databases.keys()) > 0 )
    
    def testCanShowDatabases(self):
        expected_databases = [
            'Eurexpress Biomart', 'Pancreas63', 'sequence', 'protists_variations_20', 'Prod_WHEAT', 
            'vb_sequence_mart_19', 'protists_mart_20', 'Sigenae_Oligo_Annotation_Ensembl_61', 'experiments', 
            'expression', 'WS220', 'Public_OBIOMART', 'Hsmm_Hmec', 'Prod_LMACULANSEDIT', 'ikmc', 
            'Prod_BOTRYTISEDIT', 'genomic_features', 'ontology', 'ENSEMBL_MART_ONTOLOGY', 'Prod_POPLAR_V2', 
            'Prod_', 'metazoa_mart_20', 'europhenomeannotations', 'GC_mart', 'Public_VITIS_12x', 
            'plants_variations_20', 'cildb_all_v2', 'vb_snp_mart_19', 'Prod_SCLEROEDIT', 
            'plants_mart_20', 'protists_sequence_mart_20', 'phytozome_mart', 'emma_biomart', 
            'ENSEMBL_MART_PLANT_SEQUENCE', 'htgt', 'fungi_mart_20', 'msd', 'EMAGE gene expression', 
            'Breast_mart_58', 'Sigenae Oligo Annotation (Ensembl 59)', 'functional_genomics', 'biomart', 
            'K562_Gm12878', 'cildb_inp_v2', 'biomartDB', 'vb_mart_19', 'CosmicMart', 'GRAMENE_MAP_38', 
            'ENSEMBL_MART_PLANT', 'metazoa_variations_20', 'Prod_POPLAR', 'snp', 'oncomodules', 'combinations', 
            'fungi_sequence_mart_20', 'HapMap_rel27', 'ENSEMBL_MART_PLANT_SNP', 'gmap_japonica', 
            'EMAGE browse repository', 'pride', 'Public_MAIZE', 'fungi_variations_20', 'metazoa_sequence_mart_20', 
            'Sigenae Oligo Annotation (Ensembl 56)', 'unimart', 'prod-intermart_1', 'biblioDB', 'GermOnline', 
            'vega', 'Public_TAIRV10', 'ensembl', 'EMAP anatomy ontology', 'plants_sequence_mart_20', 'REACTOME', 
            'Public_VITIS', 'QTL_MART', 'metazoa_genomic_features_mart_20', 'sequence_mart'
        ]
        self.assertTrue( expected_databases == self.server.show_databases())
    
    

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BiomartServerTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
