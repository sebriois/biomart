=============
Biomart 0.1.0
=============

Python API that consumes the biomart webservice.

What it will do:
----------------

* Show all databases of a biomart server
* Show all datasets of a biomart database
* Show attributes and filters of a biomart dataset
* Run your query formatted as a Python dict.

What it won't do:
-----------------

* Process and return the results as JSON,XML,etc. It will only return the Biomart response as TSV format.

Usage
-----

Select a dataset
::
  
  from biomart import BiomartDataset
    
  interpro = BiomartDataset( "http://www.biomart.org/biomart", {'name': 'entry'} )

Use proxy
::
  
  import os
  interpro.http_proxy = os.environ.get('http_proxy', 'http://my_http_proxy.org')

Run query: *Give me the name and abstract of interpro entry IPR027603*
::
  
  response = interpro.search({
    'filters': {
        'entry_id': 'IPR027603',
    },
    'attributes': [
        'entry_name', 'abstract'
    ]
  })
  
  # Returned format is TSV
  for line in response.iter_lines():
    print line.split("\t")
