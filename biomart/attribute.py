class BiomartAttribute(object):
    def __init__(self, params):
        self.name = params['internalName']
        self.displayName = ('displayName' in params and params['displayName'] == 'true')
        self.default = ('default' in params and params['default'] == 'true')
        self.hidden = ('hidden' in params and params['hidden'] == 'true')
    
    def __repr__(self):
        if self.default:
            return "%s (default)" % self.displayName
        return self.name
    
