import biomart
import pprint
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring, fromstring


class BiomartDataset(biomart.BiomartServer):
    """Object to handle dataset of a Biomart Server"""

    def __init__(self, url, *args, **kwargs):
        """Creates a new instance of the BiomartDataset inhering all the
        arguments from the BiomartServer object."""
        super(BiomartDataset, self).__init__(url, *args, **kwargs)

        if not 'name' in kwargs:
            raise biomart.BiomartException(
                "[BiomartDataset] 'name' argument is required.")

        self.add_property('name', kwargs['name'])
        self.add_property('displayName', kwargs.get('displayName', None))
        self.add_property('visible', (int(kwargs.get('visible', 0))) == 1)

        self._filters = {}
        self._attributes = {}

    def __repr__(self):
        """Turns the displayName to the name of the object or the name"""
        if self.displayName:
            return self.displayName
        return self.name

    @property
    def attributes(self):
        """Fetch attributes"""
        if not self._attributes:
            self.fetch_configuration()
        return self._attributes

    @property
    def filters(self):
        """Fetch filters"""
        if not self._filters:
            self.fetch_configuration()
        return self._filters

    def show_filters(self):
        """Prretty print of known datasets"""
        if not self._filters:
            self.fetch_configuration()
        pprint.pprint(self._filters.keys())

    def show_attributes(self):
        """Pretty print of known datasets"""
        if not self._attributes:
            self.fetch_configuration()
        pprint.pprint(self._attributes.keys())

    def fetch_configuration(self):
        """Fetch the configuration of the dataset of its name"""
        if self.verbose:
            print(
                "[BiomartDataset:'%s'] Fetching filters and attributes" % self.name)

        r = self.GET(type='configuration', dataset=self.name)
        xml = fromstring(r.text)

        # Filters
        for filter_description in xml.iter('FilterDescription'):
            name = filter_description.attrib['internalName']
            self._filters[name] = biomart.BiomartFilter(
                filter_description.attrib)

        # Attributes
        page_nb = 1
        for attribute_page in xml.iter('AttributePage'):
            is_hidden = attribute_page.attrib.get(
                'hideDisplay', 'false') == 'true'

            for attribute_description in attribute_page.iter('AttributeDescription'):
                name = attribute_description.attrib['internalName']
                # only attributes from the first visible page can be set as
                # default
                is_default = attribute_description.attrib.get(
                    'default', 'false') == 'true'
                if is_default and (is_hidden or page_nb > 1):
                    attribute_description.attrib['default'] = 'false'

                self._attributes[name] = biomart.BiomartAttribute(
                    attribute_description.attrib)

            if not is_hidden:
                page_nb += 1

    def count(self, params):
        """Search but counting the number of results."""
        return self.search(params, count=True)

    def search(self, params={}, header=0, count=False):
        """Search on the dataset using the parameters, and the options

        To query by strand you should use "1" (for +) and "-1" (for -).

        Example:
        import biomart
        server = biomart.BiomartServer()
        db = server.databases['ensembl']
        mus_ensembl = db.datasets['mmusculus_gene_ensembl']
        response = mus_ensembl.search({'filters': {'strand': "1"}})  # instead of '+'
        for line in response.iter_lines():
          print(line)

        Example:
        >>> import biomart
        >>> s = biomart.BiomartServer()
        >>> db = s.databases['unimart']
        >>> uniprot = db.datasets['uniprot']
        >>> response = uniprot.search({'filters': {'accession': 'Q9FMA1'}}, header=1)
        >>> for line in response.iter_lines():
        ...   print(line)
        ... 
        Accession    Protein name    Entry name    Gene name
        Q9FMA1    Pentatricopeptide repeat-containing protein At5g56310    PP433_ARATH    PCMP-E13"""
        if not self._filters or not self._attributes:
            self.fetch_configuration()

        if self.verbose:
            print(
                "[BiomartDataset:'%s'] Searching using following params:" % self.name)
            pprint.pprint(params)

        root = Element('Query')
        root.set('virtualSchemaName', self.virtual_schema)
        root.set('formatter', 'TSV')
        root.set('header', str(header))
        root.set('uniqueRows', '1')
        root.set('datasetConfigVersion', '0.6')
        if count:
            root.set('count', '1')

        dataset = SubElement(root, "Dataset")
        dataset.set('name', self.name)
        dataset.set('interface', 'default')

        filters = params.get('filters', {})
        attributes = params.get('attributes', [])

        # Add filters to XML
        if filters:
            for name, value in filters.items():
                try:
                    filter = self.filters[name]
                except KeyError:
                    raise biomart.BiomartException("The filter '%s' does not exist. Use one of: " % (
                        name, ', '.join(self.attributes.keys())))

                filter_elem = SubElement(dataset, "Filter")
                filter_elem.set('name', name)

                if filter.type == 'boolean':
                    if value == True or value.lower() == 'included' or value.lower() == 'only':
                        filter_elem.set('excluded', '0')
                    elif value == False or value.lower() == 'excluded':
                        filter_elem.set('excluded', '1')
                    else:
                        raise biomart.BiomartException(
                            "The boolean filter '%s' can only accept True, 'included', 'only', False, 'excluded'" % self.name)

                else:
                    if isinstance(value, list) or isinstance(value, tuple):
                        value = ",".join(value)
                    filter_elem.set('value', value)
        else:
            for filter in self.filters.values():
                if filter.default and filter.default_value:
                    filter_elem = SubElement(dataset)
                    filter_elem.set('name', str(filter.name))
                    if filter.type == 'boolean':
                        filter_elem.set('excluded', str(filter.default_value))
                    else:
                        filter_elem.set('value', str(filter.default_value))

        # Add attributes to XML, unless "count"
        if not count:
            if attributes:
                for attribute_name in attributes:
                    if not attribute_name in self.attributes.keys():
                        raise biomart.BiomartException(
                            "The Attribute '%s' does not exist" % attribute_name)
            else:
                attributes = [
                    attr.name for attr in self.attributes.values() if attr.default]

            if not attributes:
                raise biomart.BiomartException(
                    'No attributes selected, please select at least one')

            for attribute_name in attributes:
                attribute_elem = SubElement(dataset, "Attribute")
                attribute_elem.set('name', str(attribute_name))

        return self.GET(query=tostring(root))
