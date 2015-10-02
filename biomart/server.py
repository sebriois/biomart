import os
import pprint
from xml.etree.ElementTree import fromstring

import requests

import biomart
from .lib import PUBLIC_BIOMART_URL


class BiomartServer(object):
    def __init__(self, url = PUBLIC_BIOMART_URL, **kwargs):
        self._databases = {}
        self._datasets = {}

        if 'martservice' not in url:
            url += '/martservice'
        if not url.startswith('http://'):
            url = 'http://' + url

        self.url = url
        self.http_proxy = kwargs.get('http_proxy', os.environ.get('http_proxy', None))
        self.https_proxy = kwargs.get('https_proxy', os.environ.get('https_proxy', None))
        self._verbose = kwargs.get('verbose', False)

        self.is_alive = False
        self.assert_alive()

    def get_verbose(self):
        return self._verbose

    def set_verbose(self, value):
        if not isinstance(value, bool):
            raise biomart.BiomartException("verbose must be set to a boolean value")

        setattr(self, '_verbose', value)

        # propagate verbose state to databases and datasets objects
        for database in self._databases.values():
            database.verbose = True

        for dataset in self._datasets.values():
            dataset.verbose = True
    verbose = property(get_verbose, set_verbose)
    
    def assert_alive(self):
        if not self.is_alive:
            self.get_request()
            self.is_alive = True
            if self.verbose:
                print("[BiomartServer:'%s'] is alive." % self.url)
    
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
        if self.verbose:
            print("[BiomartServer:'%s'] Fetching databases" % self.url)

        r = self.get_request(type = 'registry')
        xml = fromstring(r.text)
        for database in xml.findall('MartURLLocation'):
            name = database.attrib['name']

            self._databases[name] = biomart.BiomartDatabase(
                server = self,
                name = name,
                display_name = database.attrib['displayName'],
                virtual_schema = database.attrib['serverVirtualSchema'],
                verbose = self._verbose
            )
    
    def fetch_datasets(self):
        if self.verbose:
            print("[BiomartServer:'%s'] Fetching datasets" % self.url)

        for database in self.databases.values():
            self._datasets.update(database.datasets)
    
    def show_databases(self):
        pprint.pprint(self.databases)
    
    def show_datasets(self):
        pprint.pprint(self.datasets)
    
    def get_request(self, **params):
        proxies = {
            'http': self.http_proxy,
            'https': self.https_proxy
        }
        if params:
            r = requests.get(self.url, params = params, proxies = proxies, stream = True)
        else:
            r = requests.get(self.url, proxies = proxies)
        r.raise_for_status()

        return r
