PUBLIC_BIOMART_URL = "http://www.biomart.org/biomart"
VERSION = "0.7.0"


class Properties(object):
    """Object to store properties"""

    def add_property(self, name, value):
        """Method to add a property as an attribute of the class"""
        # create local fget and fset functions
        fget = lambda self: self._get_property(name)
        fset = lambda self, value: self._set_property(name, value)

        # add property to self
        setattr(self.__class__, name, property(fget, fset))
        # add corresponding local variable
        setattr(self, '_' + name, value)

    def _set_property(self, name, value):
        """Auxiliar function to set the attribute name of the property"""
        setattr(self, '_' + name, value)

    def _get_property(self, name):
        """Retrieve the attribute of the desired name"""
        return getattr(self, '_' + name)
