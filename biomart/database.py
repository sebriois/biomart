import biomart
import pprint

import server


class BiomartDatabase(server.BiomartServer):
    """Object that inherits from BiomartServer that handles databases"""

    def __init__(self, url, *args, **kwargs):
        """Creates a new instance of BiomartDatabase using arguments from 
        BiomartServer object"""
        super(BiomartDatabase, self).__init__(url, *args, **kwargs)

        if not 'name' in kwargs:
            raise biomart.BiomartException(
                "[BiomartDatabase] expecting (not empty) 'name' argument")

        self.add_property('name', kwargs['name'])
        self.add_property('displayName', kwargs.get('displayName', None))
        self.add_property('visible', (int(kwargs.get('visible', 0))) == 1)
        self._datasets = {}

    def __repr__(self):
        """Turns the displayName to the name of the object or the name"""
        if self.displayName:
            return unicode(self.displayName)
        return unicode(self.name)

    @property
    def datasets(self):
        """Return the datasets available"""
        if not self._datasets:
            self.fetch_datasets()
        return self._datasets

    def show_datasets(self):
        """Pretty print of known datasets"""
        pprint.pprint(self.datasets)

    def fetch_datasets(self):
        """Fetch a dataset"""
        if self.verbose:
            print "[BiomartDatabase:'%s'] Fetching datasets" % self.name

        if not hasattr(self, '_datasets'):
            self._datasets = {}

        r = self.get(type='datasets', mart=self.name)

        for line in r.iter_lines():
            line = line.rstrip("\n").split("\t")
            if len(line) > 3:
                name = line[1]
                self._datasets[name] = biomart.BiomartDataset(
                    url=self.url,
                    http_proxy=self.http_proxy,
                    https_proxy=self.https_proxy,
                    name=name,
                    displayName=line[2],
                    visible=int(line[3]),
                    verbose=self.verbose,
                    is_alive=self.is_alive,
                    database=self.name
                )
