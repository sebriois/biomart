class BiomartAttribute(object):
    """Object that stores the parameters in name, displayName, default
     and hidden."""

    def __init__(self, params):
        """Creates a new instance of the BiomartAttribute with the selected
        parameters"""
        self.name = params['internalName']
        self.displayName = (
            'displayName' in params and params['displayName'] == 'true')
        self.default = ('default' in params and params['default'] == 'true')
        self.hidden = ('hidden' in params and params['hidden'] == 'true')
        print self.name
        print self.displayName
        print self.default
        print self.hidden

    def __repr__(self):
        """Set the reproducible name of the object"""
        if self.default:
            return "%s (default)" % self.displayName
        return self.name
