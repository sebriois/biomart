import biomart


class BiomartDatabase(object):
    def __init__(self, *args, **kwargs):
        server = kwargs.get('server', None)
        if not server:
            url = args[0]
            server = biomart.BiomartServer(url = url, **kwargs)

        self.server = server

        self.name = kwargs.get('name', None)
        if not self.name:
            raise biomart.BiomartException("[BiomartDatabase] 'name' is required")

        self.display_name = kwargs.get('display_name', self.name)
        self.virtual_schema = kwargs.get('virtual_schema', 'default')
        self.verbose = kwargs.get('verbose', False)

        self._datasets = {}
    
    def __repr__(self):
        return self.display_name
    
    @property
    def datasets(self):
        if not self._datasets:
            self.fetch_datasets()
        return self._datasets
    
    def show_datasets(self):
        import pprint
        pprint.pprint(self.datasets)

    def fetch_datasets(self):
        if self.verbose:
            print("[BiomartDatabase:'%s'] Fetching datasets" % self)

        r = self.server.get_request(type = 'datasets', mart = self.name)
        for line in r.iter_lines():
            line = line.decode('utf-8')
            if line:
                cols = line.split("\t")
                if len(cols) > 7:
                    name = cols[1]
                    self._datasets[name] = biomart.BiomartDataset(
                        server = self.server,
                        database = self,
                        name = name,
                        display_name = cols[2],
                        interface = cols[7],
                        verbose = self.verbose,
                    )
