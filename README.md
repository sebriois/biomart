Python biomart API
==================

Python package that helps to run queries against a biomart instance.

Warning:
--------
* 30/01/2014:
** This package is still under development: some expected/obvious features are not implemented yet.

What it will do:
----------------

* Show all databases of a biomart server
* Show all datasets of a biomart database
* Show attributes and filters of a biomart dataset
* Run your query formatted as a Python dict.


What it won't do:
-----------------

* Process and return the results as JSON,XML,etc. It will only return CSV or TSV format

Setup
-----

Install requirements
<pre>pip install -r requirements.txt</pre>

TODO:
<pre>
cd biomart
python setup.py build
python setup.py install
</pre>

Usage
-----

Select a dataset
<pre>
from biomart import BiomartDataset
  
interpro = BiomartDataset( "http://www.biomart.org/biomart", {'name': 'entry'} )
</pre>

Run query: <i>Give me the name and abstract of interpro entry IPR027603</i>
<pre>
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
  
</pre>
