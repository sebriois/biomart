=============
Biomart 0.9.2
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

Import Biomart module
::
  
  from biomart import BiomartServer

Connect to a Biomart Server
::
  
  server = BiomartServer( "http://www.biomart.org/biomart" )
  
  # if you are behind a proxy
  import os
  server.http_proxy = os.environ.get('http_proxy', 'http://my_http_proxy.org')

  # set verbose to True to get some messages
  server.verbose = True

Interact with the biomart server
::
  
  # show server databases
  server.show_databases() # uses pprint behind the scenes
  
  # show server datasets
  server.show_datasets() # uses pprint behind the scenes
  
  # use the 'uniprot' dataset
  uniprot = server.datasets['uniprot']

  # show all available filters and attributes of the 'uniprot' dataset
  uniprot.show_filters()  # uses pprint
  uniprot.show_attributes()  # uses pprint


Run a search
::

  # run a search with the default attributes - equivalent to hitting "Results" on the web interface.
  # this will return a lot of data.
  response = uniprot.search()
  response = uniprot.search( header = 1 ) # if you need the columns header
  
  # response format is TSV
  for line in response.iter_lines():
    line = line.decode('utf-8')
    print(line.split("\t"))
  
  # run a count - equivalent to hitting "Count" on the web interface
  response = uniprot.count()
  print(response.text)

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


Shortcut function: connect directly to a biomart dataset
*This is short in code but it might be long in time since the module needs to fetch all server's databases to find your dataset.*
::
  
  from biomart import BiomartDataset
  
  interpro = BiomartDataset( "http://www.biomart.org/biomart", name = 'entry' )
  
  response = interpro.search({
    'filters': { 'entry_id': 'IPR027603' },
    'attributes': [ 'entry_name', 'abstract' ]
  })
