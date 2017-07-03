
Biomart 0.9.2
=============

Python API that consumes the biomart webservice.

**!!!NOTE: this package is compatible with Python3 and higher versions.**

What it will do:
----------------

* Show all databases of a biomart server
* Show all datasets of a biomart database
* Show attributes and filters of a biomart dataset
* Run your query formatted as a Python dict and return the Biomart response as TSV format.

What it won't do:
-----------------

* Process and return the results as JSON,XML,etc.

Usage
-----

<pre>
# Import Biomart module
from biomart import BiomartServer

# Connect to biomart server
server = BiomartServer( "http://www.ensembl.org/biomart" )
server.verbose = True

# Check available databases
server.show_databases()

# Select a database
db = server.databases['ENSEMBL_MART_ENSEMBL']

# Check available datasets (species)
db.show_datasets()

# Select a dataset
ds = db.datasets['hsapiens_gene_ensembl']

# Show all available filters and attributes
# for the selected dataset
ds.show_filters()
ds.show_attributes()

# Run a search with the default attributes
# It is equivalent to hitting "Results" on the web interface.
# This will return a lot of data.
response = ds.search()

# If you need the columns header
response = ds.search( header = 1 )

# Response format is TSV
for line in response.iter_lines():
    line = line.decode('utf-8')
    print(line.split("\t"))

# Run a count
# It is equivalent to hitting "Count" on the web interface
response = ds.count()
print(response)

## OLD EXAMPLE BELOW

# run a search with custom filters and default attributes.
response = uniprot.search({
'filters': {
    'accession': 'Q9FMA1'
}
}, header = 1 )

response = uniprot.search({
'filters': {
    'accession': ['Q9FMA1', 'Q8LFJ9']  # ID-list specified accessions
}
}, header = 1 )

# run a search with custom filters and attributes (no header)
response = uniprot.search({
'filters': {
    'accession': ['Q9FMA1', 'Q8LFJ9']
},
'attributes': [
    'accession', 'protein_name'
]
})
</pre>

Shortcut function: connect directly to a biomart dataset
*This is short in code but it might be long in time since the module needs to fetch all server's databases to find your dataset.*
<pre>
from biomart import BiomartDataset

interpro = BiomartDataset( "http://www.biomart.org/biomart", name = 'entry' )

response = interpro.search({
'filters': { 'entry_id': 'IPR027603' },
'attributes': [ 'entry_name', 'abstract' ]
})
</pre>
