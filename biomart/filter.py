class BiomartFilter(object):
    def __init__(self, params):
        self.name = params['internalName']
        self.displayName = ('displayName' in params and params['displayName'] == 'true')
        self.type = ('type' in params and params['type'] == 'true')
        self.default = ('default' in params and params['default'] == 'true')
        self.default_value = 'defaultValue' in params and params['defaultValue'] or None
        self.hidden = ('hidden' in params and params['hidden'] == 'true')
    
    def __repr__(self):
        return self.name
    
