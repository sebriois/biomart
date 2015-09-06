import biomart
import pprint
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

import database
import server


class BiomartDataset(database.BiomartDatabase):  # server.BiomartServer
    """Object to handle dataset of a Biomart Server"""

    def __init__(self, url, *args, **kwargs):
        """Creates a new instance of the BiomartDataset inhering all the 
        arguments from the BiomartServer object."""
        super(BiomartDataset, self).__init__(url, *args, **kwargs)

        if not 'name' in kwargs:
            msg = "[BiomartDataset] expecting (not empty) 'name' argument"
            raise biomart.BiomartException(msg)

        self.add_property('name', kwargs['name'])
        self.add_property('displayName', kwargs.get('displayName', None))
        self.add_property('visible', (int(kwargs.get('visible', 0))) == 1)
        self.database = kwargs["database"]
        self._filters = []
        self._attributes = []

    def __repr__(self):
        """Set the value to reproduce when printing the object"""
        if self.displayName:
            return unicode(self.displayName)
        return unicode(self.name)

    @property
    def attributes(self):
        """Fetch the attributes"""
        if not self._attributes:
            self.fetch_configuration()
        return self._attributes

    @property
    def filters(self):
        """Fetch the filters"""
        if not self._filters:
            self.fetch_configuration()
        return self._filters

    def show_filters(self):
        """Prints pretty the filters it has"""
        if not self._filters:
            self.fetch_configuration()
        pprint.pprint(self._filters)

    def show_attributes(self):
        """Prints pretty the attributes it has"""
        if not self._attributes:
            self.fetch_configuration()
        pprint.pprint(self._attributes)

    def fetch_configuration(self):
        """Fetch the configuration of the dataset of its name"""
        if self.verbose:
            print "[BiomartDataset:'%s'] Fetching filters and attributes" % self.name

        r = self.get(type='configuration', dataset=self.name)
        xml = fromstring(r.text)

        # Fetch filters options
        for filter_description in xml.iter('FilterDescription'):
            #             name = filter_description.attrib['internalName']
            self._filters.append(biomart.BiomartFilter(
                filter_description.attrib))

        # Fetch attributes options
        for attribute_description in xml.iter('AttributeDescription'):
            #             name = attribute_description.attrib['internalName']
            self._attributes.append(biomart.BiomartAttribute(
                attribute_description.attrib))
        if self.verbose:
            print "[BiomartDataset:'%s'] Configuration fetch correctly" % self.name

    def count(self, params={}):
        """Search but counting the number of results."""
        return self.search(params, count=True)

    def search(self, params={}, header=0, count=False):
        """Search using the parameters, and the options"""
        if not self._filters or not self._attributes:
            self.fetch_configuration()

        if self.verbose:
            print "[BiomartDataset:'%s'] Searching using following params:" % self.name
            pprint.pprint(params)

        root = Element('Query')
        root.set('virtualSchemaName', 'default')
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
            try:
                filters.items()
            except AttributeError:
                msg = "The filters value should be a dictionary"
                raise biomart.BiomartException(msg)

            for name, value in filters.items():
                try:
                    filter_ = self.filters[name]
                except KeyError:
                    msg = "The filter '%s' does not exist. Use one of: " % (
                        name, ', '.join(self.attributes.keys()))
                    raise biomart.BiomartException()

                filter_elem = SubElement(dataset, "Filter")
                filter_elem.set('name', name)

                if filter_.type == 'boolean':
                    if value == True or value.lower() in ['included', 'only']:
                        filter_elem.set('excluded', '0')
                    elif value == False or value.lower() == 'excluded':
                        filter_elem.set('excluded', '1')
                    else:
                        msg = "The boolean filter '%s' can only accept True, " \
                            "'included', 'only', False, 'excluded'" % self.name
                        raise biomart.BiomartException(msg)

                else:
                    if isinstance(value, list) or isinstance(value, tuple):
                        value = ",".join(value)
                    filter_elem.set('value', value)
        else:
            for filter_ in self.filters.values():
                if filter.default and filter.default_value:
                    filter_elem = SubElement(dataset)
                    filter_elem.set('name', str(filter.name))
                    if filter.type == 'boolean':
                        filter_elem.set('excluded', str(filter.default_value))
                    else:
                        filter_elem.set('value', str(filter.default_value))

        # Add attributes to XML, unless "count"
        if not count:
            if attributes and isinstance(attributes, list):
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

        return self.get(query=tostring(root)).rstrip()
