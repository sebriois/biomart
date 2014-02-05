import requests
from xml.etree.ElementTree import fromstring
import biomart

class BiomartServer(object):
    def __init__(self, url, http_proxy = '', https_proxy = ''):
        if not 'martservice' in url:
            url += '/martservice'
        if not 'http://' in url:
            url = 'http://' + url
        
        self.url = url
        self.proxies = { 'http': http_proxy, 'https': https_proxy }
        
        self._databases = {}
        self._datasets = {}
    
    def get_http_proxy(self):
        return self.proxies['http']
    def set_http_proxy(self, http_proxy):
        self.proxies['http'] = http_proxy
    http_proxy = property(get_http_proxy, set_http_proxy)
    
    def get_https_proxy(self):
        return self.proxies['https']
    def set_https_proxy(self, https_proxy):
        self.proxies['https'] = https_proxy
    https_proxy = property(get_https_proxy, set_https_proxy)
    
    def is_alive(self):
        r = requests.get( self.url, proxies = self.proxies )
        return r.status_code == requests.codes.ok
    
    def assert_alive(self):
        if not self.is_alive():
            raise biomart.BiomartException( "Server is not alive or could not be reached." )
    
    @property
    def databases(self):
        if not self._databases:
            self.fetch_databases()
        return self._databases
    
    @property
    def datasets(self):
        if not self._datasets:
            self.fetch_datasets()
        return self._datasets
    
    def fetch_databases(self):
        self.assert_alive()
        
        r = requests.get( self.url, params = { 'type': 'registry' }, proxies = self.proxies )
        xml = fromstring(r.text)
        for child in xml:
            if child.tag == 'MartURLLocation':
                database = biomart.BiomartDatabase(
                    url         = self.url, 
                    params      = child.attrib, 
                    http_proxy  = self.http_proxy, 
                    https_proxy = self.https_proxy
                )
                self._databases[ child.attrib['name'] ] = database
    
    def fetch_datasets(self):
        self.assert_alive()
        
        for database in self.databases.values():
            self._datasets.update( database.datasets )
    
    def show_databases(self):
        if not self._databases:
            self.fetch_databases()
        
        return self._databases.keys()
    
    def show_datasets(self):
        if not self._datasets:
            self.fetch_datasets()
        
        return self._datasets.keys()
    
