class BiomartFilter(object):
    """Store the filter parameters of a dataset"""

    def __init__(self, params):
        """Given the attributes of a request store them as attributes of these class"""
        for name, value in params.iteritems():
            if name == "internalName":
                self.name = params['internalName']
                continue
            else:
                setattr(self, name, value)

    def __repr__(self):
        """Set the reproducibility name of the object"""
        return self.name
