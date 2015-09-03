PUBLIC_BIOMART_URL = "http://www.biomart.org/biomart"
VERSION = "0.6.0"


class Properties(object):

    def add_property(self, name, value):
        # create local fget and fset functions
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)

        # add property to self
        setattr(self.__class__, name, property(fget, fset))
        # add corresponding local variable
        setattr(self, '_' + name, value)

    def _set_property(self, name, value):
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        return getattr(self, '_' + name)
