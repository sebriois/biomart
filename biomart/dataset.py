from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import pprint
import biomart


class BiomartDataset(object):
    def __init__(self, *args, **kwargs):
        # dataset specific attributes
        self.name = kwargs.get('name', None)
        if not self.name:
            raise biomart.BiomartException("[BiomartDataset] 'name' is required")

        self.display_name = kwargs.get('display_name', self.name)
        self.interface = kwargs.get('interface', 'default')
        self.verbose = kwargs.get('verbose', False)

        # get related biomart server
        server = kwargs.get('server', None)
        if not server:
            url = args[0]
            server = biomart.BiomartServer(url = url, **kwargs)
        self.server = server

        # get related biomart database
        self.database = kwargs.get('database', None)

        self._filters = {}
        self._attribute_pages = {}

    def __repr__(self):
        return self.display_name

    @property
    def attributes(self):
        """
        A dictionary mapping names of attributes to BiomartAttribute instances.

        This causes overwriting errors if there are diffferent pages which use
        the same attribute names, but is kept for backward compatibility.
        """
        if not self._attribute_pages:
            self.fetch_attributes()
        result = {}
        for page in self._attribute_pages.values():
            result.update(page.attributes)
        return result


    @property
    def attribute_pages(self):
        """
        A dictionary mapping pages of attributes to BiomartAttributePage instances.
        Lists of attributes for particular pages can be accessed by 'attributes'
        field of pages instances.
        """
        if not self._attribute_pages:
            self.fetch_attributes()
        return self._attribute_pages


    @property
    def filters(self):
        if not self._filters:
            self.fetch_filters()
        return self._filters

    def show_filters(self):
        pprint.pprint(self.filters)

    def show_attributes(self):
        pprint.pprint(self.attributes)

    def show_attributes_by_page(self):
        pprint.pprint(self.attribute_pages)

    def fetch_filters(self):
        if self.verbose:
            print("[BiomartDataset:'%s'] Fetching filters" % self.name)

        r = self.server.get_request(type="filters", dataset=self.name)
        for line in r.iter_lines():
            line = line.decode('utf8')
            if line:
                line = line.split("\t")
                self._filters[line[0]] = biomart.BiomartFilter(
                    name = line[0],
                    display_name = line[1],
                    accepted_values = line[2],
                    filter_type = line[5],
                )


        # retrieve additional filters from the dataset configuration page
        r = self.server.get_request(type="configuration", dataset=self.name)
        xml = fromstring(r.text)

        for attribute_page in xml.findall('./AttributePage'):

            for attribute in attribute_page.findall('./*/*/AttributeDescription[@pointerFilter]'):
                name = attribute.get('pointerFilter')

                if not name in self._filters:
                    self._filters[name] = biomart.BiomartFilter(
                        name = name,
                        display_name = attribute.get('displayName') or name,
                        accepted_values = '',
                        filter_type = '',
                    )

    def fetch_attributes(self):
        if self.verbose:
            print("[BiomartDataset:'%s'] Fetching attributes" % self.name)

        # retrieve default attributes from the dataset configuration page
        r = self.server.get_request(type="configuration", dataset=self.name)
        xml = fromstring(r.text)

        for idx, attribute_page in enumerate(xml.findall('./AttributePage')):

            name = attribute_page.get('internalName')
            display_name = attribute_page.get('displayName')

            default_attributes = []

            for attribute in attribute_page.findall('./*/*/AttributeDescription[@default="true"]'):
                default_attributes.append(attribute.get('internalName'))

            self._attribute_pages[name] = biomart.BiomartAttributePage(
                name,
                display_name = display_name,
                default_attributes = default_attributes,
                is_default = (idx == 0)  # first attribute page fetched is considered default
            )

        # grab attribute details
        r = self.server.get_request(type="attributes", dataset=self.name)
        for line in r.iter_lines():
            line = line.decode('utf8')
            if line:
                line = line.split("\t")
                page = line[3]
                name = line[0]

                if page not in self._attribute_pages:
                    self._attribute_pages[page] = biomart.BiomartAttributePage(page)
                    if self.verbose:
                        print("[BiomartDataset:'%s'] Warning: attribute page '%s' is not specified in server's configuration" % (self.name, page))

                attribute = biomart.BiomartAttribute(name=name, display_name=line[1])
                self._attribute_pages[page].add(attribute)

    def search(self, params = {}, header = 0, count = False):
        if not isinstance(params, dict):
            raise biomart.BiomartException("'params' argument must be a dict")

        if self.verbose:
            print("[BiomartDataset:'%s'] Searching using following params:" % self.name)
            pprint.pprint(params)

        # read filters and attributes from params
        filters = params.get('filters', {})
        attributes = params.get('attributes', [])

        # check filters
        for filter_name, filter_value in filters.items():
            dataset_filter = self.filters.get(filter_name, None)

            if not dataset_filter:
                if self.verbose:
                    self.show_filters()
                raise biomart.BiomartException("The filter '%s' does not exist." % filter_name)

            if len(dataset_filter.accepted_values) > 0 and filter_value not in dataset_filter.accepted_values:
                error_msg = "The value '%s' for filter '%s' cannot be used." % (filter_value, filter_name)
                error_msg += " Use one of: [%s]" % ", ".join(map(str, dataset_filter.accepted_values))
                raise biomart.BiomartException(error_msg)

        # check attributes unless we're only counting
        if not count:

            # discover attributes and pages
            self.fetch_attributes()

            # no attributes given, use default attributes
            if not attributes and self._attribute_pages:
                # get default attribute page
                page = next(filter(lambda attr_page: attr_page.is_default, self._attribute_pages.values()))
                
                # get default attributes from page
                attributes = [a.name for a in page.attributes.values() if a.is_default]

                # there is no default attributes, get all attributes from page
                if not attributes:
                    attributes = [a.name for a in page.attributes.values()]

            # if no default attributes have been defined, raise an exception
            if not attributes:
                raise biomart.BiomartException("at least one attribute is required, none given")

            for attribute_name in attributes:
                found = False
                for page in self._attribute_pages.values():
                    if attribute_name in page.attributes.keys():
                        found = True
                        break
                if not found:
                    if self.verbose:
                        self.show_attributes()
                    raise biomart.BiomartException("The attribute '%s' does not exist." % attribute_name)

            # guess the attribute page and check if all attributes belong to it.
            guessed_page = None

            for tested_page in self._attribute_pages.values():
                if set(attributes).issubset(tested_page.attributes.keys()):
                    guessed_page = tested_page
                    break

            if guessed_page is None:
                # selected attributes must belong to the same attribute page.
                if self.verbose:
                    self.show_attributes()
                raise biomart.BiomartException("You must use attributes that belong to the same attribute page.")
        # filters and attributes looks ok, start building the XML query
        root = Element('Query')
        root.attrib.update({
            'virtualSchemaName': self.database.virtual_schema,
            'formatter': 'TSV',
            'header': str(header),
            'uniqueRows': '1',
            'datasetConfigVersion': '0.6',
            'count': count is True and '1' or ''
        })

        dataset = SubElement(root, "Dataset")
        dataset.attrib.update({
            'name': self.name,
            'interface': self.interface
        })

        # Add filters to the XML query
        for filter_name, filter_value in filters.items():
            dataset_filter = self.filters[filter_name]

            filter_elem = SubElement(dataset, "Filter")
            filter_elem.set('name', filter_name)

            if 'boolean_list' == dataset_filter.filter_type:
                if filter_value is True or filter_value.lower() in ('included', 'only'):
                    filter_elem.set('excluded', '0')
                elif filter_value is False or filter_value.lower() == 'excluded':
                    filter_elem.set('excluded', '1')
            else:
                if isinstance(filter_value, list) or isinstance(filter_value, tuple):
                    filter_value = ",".join(map(str, filter_value))
                filter_elem.set('value', str(filter_value))

        # Add attributes to the XML query, unless we're only counting
        if not count:
            for attribute_name in attributes:
                attribute_elem = SubElement(dataset, "Attribute")
                attribute_elem.set('name', str(attribute_name))

        if self.verbose:
            print("[BiomartDataset] search query:\n%s" % tostring(root))

        return self.server.get_request(query = tostring(root))

    def count(self, params = {}):
        r = self.search(params, count = True)
        return int(r.text.strip())
