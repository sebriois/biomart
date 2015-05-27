Biomart 0.5.0
=============

Python API that consumes the biomart webservice.

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
import biomart
web = "http://www.biomart.org/biomart"
name = 'hsapiens_gene_ensembl'
server = biomart.BiomartServer(web)
server.set_verbose(True)
server.show_databases()
ensembl_ds = biomart.BiomartDataset(web, name=name)
ensembl_ds.fetch_configuration()
</pre>
Import Biomart module
<pre>
from biomart import BiomartServer
</pre>
Connect to a Biomart Server
<pre>
server = BiomartServer( "http://www.biomart.org/biomart" )

# if you are behind a proxy
import os
server.http_proxy = os.environ.get('http_proxy', 'http://my_http_proxy.org')
</pre>

Interact with the biomart server
<pre>
from biomart import BiomartServer

server = BiomartServer("http://www.biomart.org/biomart")
# show server databases
#server.show_databases()

# show server datasets
#server.show_datasets()

# use the 'uniprot' dataset
uniprot = server.datasets['uniprot']
# show all available filters and attributes of the 'uniprot' dataset
uniprot.show_filters()
uniprot.show_attributes()
# run a search with the default filters and attributes - equivalent to hitting "Results" on the web interface.
# this will return a lot of data.
response = uniprot.search()
response = uniprot.search(header=1) # if you need the columns header
# response format is TSV

params = {}
# run a count with the default filters and attributes - equivalent to hitting "Count" on the web interface
response = uniprot.count(params) #TODO: Fix this ;)
print response.text.rstrip()


# run a search with custom filters and default attributes.
response = uniprot.search({
  'filters': {
      'accession': 'Q9FMA1'
  }
}, header=1)
for line in response.iter_lines():
    print line
response = uniprot.search({
  'filters': {
      'accession': ['Q9FMA1', 'Q8LFJ9']  # ID-list specified accessions
  }
}, header=1)
for line in response.iter_lines():
    print line
# run a search with custom filters and attributes
response = uniprot.search({
  'filters': {
      'accession': ['Q9FMA1', 'Q8LFJ9']
  },
  'attributes': [
      'accession', 'protein_name'
  ]
})
for line in response.iter_lines():
    print line
</pre>
