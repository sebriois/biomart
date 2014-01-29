#!/usr/bin/env python

from biomart import BiomartDataset

interpro = BiomartDataset( "http://www.biomart.org/biomart", {'name': 'entry'} )
response = interpro.search({
    'filters': {'entry_id': 'IPR027603'},
    'attributes': ['entry_id', 'entry_name']
})

for line in response.iter_lines():
    print line
