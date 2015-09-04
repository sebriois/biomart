class BiomartFilter(object):
    """Class that filter a dataset given paramaters"""

    def __init__(self, params):
        """Given params create a dictionary with them using some default values"""
        self.name = params['internalName']
        self.displayName = (
            'displayName' in params and params['displayName'] == 'true')
        self.type = ('type' in params and params['type'] == 'true')
        self.default = ('default' in params and params['default'] == 'true')
        self.default_value = (
            'defaultValue' in params and params['defaultValue'] or None)
        self.hidden = ('hidden' in params and params['hidden'] == 'true')

    def __repr__(self):
        """Returns the name of the filter"""
        return self.name
