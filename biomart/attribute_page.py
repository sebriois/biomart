class BiomartAttributePage(object):
    def __init__(self, name, display_name=None, attributes=None, default_attributes=None, is_default=False):
        self.name = name
        self.display_name = display_name or name
        self.attributes = attributes if attributes else {}
        self.default_attributes = default_attributes if default_attributes else []
        self.is_default = is_default

    def add(self, attribute):
        attribute.is_default = attribute.name in self.default_attributes
        self.attributes[attribute.name] = attribute

    def __repr__(self):
        return "'%s': (attributes: %s, defaults: %s)" % (self.display_name, self.attributes, repr(self.default_attributes))
