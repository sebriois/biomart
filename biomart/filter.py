class BiomartFilter(object):
    def __init__(self, params):
        self.name = params['internalName']
        self.displayName = params['displayName']
        self.type = params['type']
        self.default = ('default' in params and params['default'] == 'true')
        self.default_value = 'defaultValue' in params and params['defaultValue'] or None
        self.hidden = ('hidden' in params and params['hidden'] == 'true')
    
    def __repr__(self):
        return self.name
    
