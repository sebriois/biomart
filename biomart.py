import requests

from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring, fromstring

class BiomartServer(object):
    def __init__(self, url, http_proxy = '', https_proxy = ''):
        if not 'martservice' in url:
            url += '/martservice'
        if not 'http://' in url:
            url = 'http://' + url
        
        self._url = url
        self._proxies = { 'http': http_proxy, 'https': https_proxy }
        self._is_alive = None
        self._databases = {}
        self._datasets = {}
    
    def get_proxy(self):
        return self._proxies['http']
    def set_proxy(self, http_proxy):
        self._proxies['http'] = http_proxy
    http_proxy = property(get_proxy, set_proxy)
    
    @property
    def url(self):
        return self._url
    
    @property
    def databases(self):
        if not self._databases:
            self.snif_databases()
        
        return self._databases
    
    @property
    def datasets(self):
        if not self._datasets.keys():
            self.snif_datasets()
        
        return self._datasets
    
    def assert_alive(self):
        if not self.is_alive():
            raise Exception( "Server is not alive or could not be reached" )
    
    def is_alive(self):
        if not self._is_alive:
            r = requests.get( self._url, proxies = self._proxies )
            self._is_alive = (r.status_code == requests.codes.ok)
        return self._is_alive
    
    def snif_databases(self):
        self.assert_alive()
        r = requests.get( self._url, params = { 'type': 'registry' }, proxies = self._proxies )
        xml = fromstring(r.text)
        for child in xml:
            if child.tag == 'MartURLLocation':
                self._databases[ child.attrib['name'] ] = BiomartDatabase( self._url, child.attrib )
    
    def snif_datasets(self):
        for database in self.databases.values():
            self._datasets.update( database.datasets )
    
class BiomartDatabase(BiomartServer):
    def __init__(self, url, params):
        super(BiomartDatabase, self).__init__(url)
        
        self._name = params['name']
        self._displayName = params['displayName']
        self._visible = params['visible'] == 1
        self._datasets = {}
    
    def __repr__(self):
        return "%s (visible: %s)" % (self._displayName, self._visible)
    
    @property
    def datasets(self):
        if not self._datasets:
            self.snif_datasets()
        
        return self._datasets
    
    def snif_datasets(self):
        self.assert_alive()
        print "Retrieving datasets for %s" % self._name
        r = requests.get( self._url, params = { 'type': 'datasets', 'mart': self._name }, proxies = self._proxies )
        for line in r.iter_lines():
            line = line.strip().split("\t")
            if len(line) > 3:
                params = {
                    'name': line[1],
                    'displayName': line[2],
                    'visible': int(line[3])
                }
                self._datasets[params['name']] = BiomartDataset( self._url, params )
        print "Done."

class BiomartDataset(BiomartServer):
    def __init__(self, url, params):
        super(BiomartDataset, self).__init__(url)
        self._name = params['name']
        if not self._name:
            raise Exception( "Dataset 'name' is required in params" )
        
        self._displayName = 'displayName' in params and params['displayName']
        self._visible = 'visible' in params and params['visible'] == 1
        self._filters = {}
        self._attributes = {}
    
    def __repr__(self):
        return "%s (visible: %s)" % (self._displayName, self._visible)
    
    @property
    def filters(self):
        if not self._filters:
            self.get_configuration()
        
        return self._filters
    
    @property
    def attributes(self):
        if not self._attributes:
            self.get_configuration()
        
        return self._attributes
    
    def get_configuration(self):
        self.assert_alive()
        
        if self._attributes and self._filters:
            return
        
        print "Loading filters and attributes for %s" % (self._displayName and self._displayName or self._name )
        r = requests.get( self._url, params = { 'type': 'configuration', 'dataset': self._name }, proxies = self._proxies )
        
        xml = fromstring( r.text )
        
        # Filters
        for filter_description in xml.iter( 'FilterDescription' ):
            name = filter_description.attrib['internalName']
            self._filters[name] = BiomartFilter( filter_description.attrib )
        
        # Attributes
        for attribute_description in xml.iter( 'AttributeDescription' ):
            name = attribute_description.attrib['internalName']
            self._attributes[name] = BiomartAttribute( attribute_description.attrib )
    
    def count( self, params ):
        return self.search( params, count = True )
    
    def search( self, params, count = False ):
        self.assert_alive()
        self.get_configuration()
        print "Executing query..."
        
        root = Element( 'Query' )
        root.set('virtualSchemaName', 'default')
        root.set('formatter', 'TSV')
        root.set('header', '0')
        root.set('uniqueRows', '1')
        root.set('datasetConfigVersion', '0.6')
        if count:
            root.set('count', '1')
        
        self.to_xml( root, filters = params['filters'], attributes = params['attributes'], count = count )
        return requests.get( self.url, params = { 'query': tostring( root ) }, proxies = self._proxies )
    
    def to_xml( self, root_element, filters = {}, attributes = [], count = False ):
        dataset = SubElement( root_element, "Dataset" )
        dataset.set( 'name', self._name )
        dataset.set( 'interface', 'default' )
        
        # Add filters to XML
        if filters:
            for name, value in filters.items():
                try:
                    filter = self.filters[name]
                except KeyError:
                    print self.attributes.keys()
                    raise Exception( "The filter '%s' does not exist" % name )
                
                filter_elem = SubElement( dataset, "Filter" )
                filter_elem.set( 'name', name )
                
                if filter.type == 'boolean':
                    if value == True or value.lower() == 'included' or value.lower() == 'only':
                        filter_elem.set( 'excluded', 0 )
                    elif value == False or value.lower() == 'excluded':
                        filter_elem.set( 'excluded', 1 )
                    else:
                        raise Exception( "The boolean filter '%s' can only accept True, 'included', 'only', False, 'excluded'" % self.name )
                else:
                    if isinstance( value, list ) or isinstance( value, tuple ):
                        value = ",".join( value )
                    filter_elem.set( 'value', value )
                
                filter_elem.set( 'value', value )
        else:
            for filter in self.filters.values():
                if filter.default and filter.default_value:
                    filter_elem = SubElement( dataset )
                    filter_elem.set( 'name', filter.name )
                    if filter.type == 'boolean':
                        filter_elem.set( 'excluded', filter.default_value )
                    else:
                        filter_elem.set( 'value', filter.default_value )
        
        # Add attributes to XML, unless "count"
        if not count:
            if attributes:
                for attribute_name in attributes:
                    if not attribute_name in self.attributes.keys():
                        raise Exception( "The Attribute '%s' does not exist" % attribute_name )
                    attribute_elem = SubElement( dataset, "Attribute" )
                    attribute_elem.set( 'name', attribute_name )
            else:
                for attribute in self.attributes.values():
                    if attribute.default:
                        attribute_elem = SubElement( dataset, "Attribute" )
                        attribute_elem.set( 'name', attribute.name )
    
class BiomartAttribute(object):
    def __init__(self, params):
        self.name = params['internalName']
        self.displayName = params['displayName']
        self.default = ('default' in params and params['default'] == 'true')
        self.hidden = ('hidden' in params and params['hidden'] == 'true')
    
    def __repr__(self):
        return self.displayName
    
class BiomartFilter(object):
    def __init__(self, params):
        self.name = params['internalName']
        self.displayName = params['displayName']
        self.type = params['type']
        self.default = ('default' in params and params['default'] == 'true')
        self.default_value = 'defaultValue' in params and params['defaultValue'] or None
        self.hidden = ('hidden' in params and params['hidden'] == 'true')
    
    def __repr__(self):
        return self.displayName
    