class BiomartAttribute(object):
    def __init__(self, name, display_name, attribute_page, is_default = False):
        self.name = name
        self.display_name = display_name
        self.attribute_page = attribute_page
        self.is_default = is_default

    def __repr__(self):
        return "'%s' (page: %s, default: %s)" % (self.display_name, self.attribute_page, self.is_default)
