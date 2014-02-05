import requests
import biomart

class BiomartDatabase(biomart.BiomartServer):
    def __init__(self, url, params, *args, **kwargs):
        super(BiomartDatabase, self).__init__(url, *args, **kwargs)
        
        if not 'name' in params:
            raise biomart.BiomartException("'name' arg must be specified.")
        
        self.name        = params['name']
        self.displayName = params.get('displayName', None)
        self.visible     = (params.get('visible', 0) == 1)
        self._datasets   = {}
    
    def __repr__(self):
        return self.name
    
    @property
    def datasets(self):
        if not self._datasets:
            self.fetch_datasets()
        return self._datasets
    
    def fetch_datasets(self):
        self.assert_alive()
        
        r = requests.get( self.url, params = { 'type': 'datasets', 'mart': self.name }, proxies = self.proxies )
        for line in r.iter_lines():
            line = line.rstrip("\n").split("\t")
            if len(line) > 3:
                params = {
                    'name': line[1],
                    'displayName': line[2],
                    'visible': int(line[3])
                }
                self._datasets[params['name']] = biomart.BiomartDataset( self.url, params, http_proxy = self.http_proxy )
        
    
