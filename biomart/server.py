# -*- coding: utf-8 -*-
import biomart
import os
import pprint
import requests
from xml.etree.ElementTree import fromstring

from lib import Properties, PUBLIC_BIOMART_URL


class BiomartServer(Properties):
    """Object to handle connection to Biomart servers"""

    def __init__(self, url=PUBLIC_BIOMART_URL, *args, **kwargs):
        """Creates a new instance connecting to the biomart website.
        By default use the biomart url"""
        if not 'martservice' in url:
            url += '/martservice'
        if not 'http://' in url:
            url = 'http://' + url

        self.add_property('url', url)
        self.add_property(
            'http_proxy', kwargs.get('http_proxy',  os.environ.get('http_proxy',  None)))
        self.add_property('https_proxy', kwargs.get(
            'https_proxy',  os.environ.get('https_proxy',  None)))
        self.add_property('is_alive', kwargs.get('is_alive', False))
        self._verbose = kwargs.get('verbose', False)
        self.assert_alive()

    def get_verbose(self):
        """Return if verbose is set or not"""
        return self._verbose

    def set_verbose(self, value):
        """"""
        if not isinstance(value, bool):
            raise biomart.BiomartException(
                "verbose must be set to a boolean value")
        setattr(self, '_verbose', value)

        # propagate verbose state to databases and datasets objects
        if hasattr(self, '_databases'):
            for database in self._databases.values():
                database.verbose = True
        if hasattr(self, '_datasets'):
            for dataset in self._datasets.values():
                dataset.verbose = True
    verbose = property(get_verbose, set_verbose)

    def assert_alive(self):
        """Set the connection to the server alive"""
        if not self.is_alive:
            self.GET()
            self.is_alive = True
            if self.verbose:
                print "[BiomartServer:'%s'] is alive." % self.url
        else:
            print "[BiomartServer:'%s'] is already alive." % self.url

    @property
    def databases(self):
        """Return a dictionary with the available databases and a description
         of them."""
        if not hasattr(self, '_databases'):
            self._databases = {}
            self.fetch_databases()
        return self._databases

    @property
    def datasets(self):
        """Prints the available datasets as a dictionary:
        The name of the database as a key and a simple description as a value"""
        if not hasattr(self, '_datasets'):
            self._datasets = {}
            self.fetch_datasets()
        return self._datasets

    def fetch_databases(self):
        """Fetch the name and description of the databases."""
        if self.verbose:
            print "[BiomartServer:'%s'] Fetching databases" % self.url

        if not hasattr(self, '_databases'):
            self._databases = {}

        r = self.GET(type='registry')
        xml = fromstring(r.text)
        for child in xml.findall('MartURLLocation'):
            name = child.attrib['name']

            self._databases[name] = biomart.BiomartDatabase(
                url=self.url,
                http_proxy=self.http_proxy,
                https_proxy=self.https_proxy,
                name=name,
                displayName=child.attrib['displayName'],
                visible=child.attrib['visible'],
                verbose=self.verbose,
                is_alive=self.is_alive
            )
        if self.verbose:
            print "[BiomartServer:'%s'] Successfully fetch databases" % self.url

    def fetch_datasets(self):
        """Fetch datasets of the databases"""
        # TODO: Add the possibility to obtain the datasets of a single database
        if self.verbose:
            print "[BiomartServer:'%s'] Fetching datasets" % self.url

        if not hasattr(self, '_datasets'):
            self._datasets = {}

        for database in self.databases.values():
            self._datasets.update(database.datasets)

        if self.verbose:
            print "[BiomartServer:'%s'] Successfully fetch datasets" % self.url

    def show_databases(self):
        """Show a dictionary with the name of the database and a description"""
        pprint.pprint(self.databases)

    def show_datasets(self):
        """Prints a table with information about each dataset. The information is:
        Type of data, ¿name of the dataset?, ¿description of the dataset?, ¿?, 
        ¿version?, columns?, rows?, permision, datestamp
        Example:
        TableSet    pinfestans_eg_snp    Phytophthora infestans variations 
        (ASM14294v1)    1    ASM14294v1    200    50000    default    2014-12-18 15:44:39"""
        pprint.pprint(self.datasets)

    def get(self, **params):
        """Test if the server and the databases return the right status code"""
        proxies = {
            'http': self.http_proxy,
            'https': self.https_proxy
        }
        if params:
            r = requests.get(
                self.url, params=params, proxies=proxies, stream=True)
        else:
            r = requests.get(self.url, proxies=proxies)
        r.raise_for_status()

        return r
