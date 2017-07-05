=============
Biomart 1.0.0
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

::
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
	#response = ds.search()

	# If you need the columns header
	#response = ds.search( header = 1 )

	# Response format is TSV
	for line in response.iter_lines():
	    line = line.decode('utf-8')
	    print(line.split("\t"))

	# Run a count
	# It is equivalent to hitting "Count" on the web interface
	response = ds.count()
	print(response)

	# run a search with custom filters and default attributes.
	response = ds.search({
	    'filters':{
	        'ensembl_gene_id':'ENSG00000132646'
	    }
	}, header = 1)

	response = ds.search({
	    'filters':{
	        'ensembl_gene_id':['ENSG00000132646', 'ENSG00000141510']
	    }
	}, header = 1)

	# run a search with custom filters and attributes (no header)
	response = ds.search({
	    'filters':{
	        'ensembl_gene_id':['ENSG00000132646', 'ENSG00000141510']
	    },
	    'attributes':[
	        'ensembl_gene_id',              # Gene ID
	        'chromosome_name',              # Chromosome
	        'start_position',               # Start
	        'end_position',                 # End
	        'strand',                       # Strand
	        'transcript_count',             # Number of transcripts
	        'percentage_gene_gc_content'    # GC content percentage
	    ]
	}, header = 1)

	# To convert the response variable to a more readable format
	# let's take advantage of the numpy and pandas libraries
	import numpy as np
	import pandas as pd

	# Convert to easily accessible numpy array
	response = np.array([row.split('\t')
	    for row in response.text.strip().split('\n')])

	# Convert to easy-to-read pandas dataframe
	# With header line
	response = pd.DataFrame(response[1:,:], columns = response[0])
	# Without header line
	response = pd.DataFrame(response)

	print(response)
