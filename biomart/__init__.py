from server import BiomartServer
from database import BiomartDatabase
from dataset import BiomartDataset
from filter import BiomartFilter
from attribute import BiomartAttribute

TEST_URL="http://www.biomart.org/biomart"

class BiomartException(Exception):
    pass
