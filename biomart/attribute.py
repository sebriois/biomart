class BiomartAttribute(object):
    """Object that stores the attributes parameters of a dataset"""

    def __init__(self, params):
        """Creates a new instance of the BiomartAttribute."""

        for name, value in params.iteritems():
            if name == "internalName":
                self.name = params['internalName']
                continue
            else:
                setattr(self, name, value)

    def __repr__(self):
        """Set the reproducibility name of the object"""
        return self.name
