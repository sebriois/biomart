class BiomartFilter(object):
    """Store the filter parameters of a dataset"""

    def __init__(self, params):
        """Given the attributes of a request store them as attributes of these class"""
        self.name = params['internalName']
        self.displayName = (
            'displayName' in params and params['displayName'] == 'true')
        self.type = ('type' in params and params['type'] == 'true')
        self.default = ('default' in params and params['default'] == 'true')
        self.default_value = 'defaultValue' in params and params[
            'defaultValue'] or None
        self.hidden = ('hidden' in params and params['hidden'] == 'true')

    def __repr__(self):
        """Set the reproducibility name of the object"""
        return self.name
