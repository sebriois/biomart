class BiomartAttribute(object):
    def __init__(self, name, display_name, is_default = False):
        self.name = name
        self.display_name = display_name
        self.is_default = is_default

    def __repr__(self):
        return "'%s' (default: %s)" % (self.display_name, self.is_default)
