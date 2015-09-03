import test_server
import test_database
import test_dataset
import test_filter
import test_attribute
import unittest

def suite():
    import doctest
    suite = unittest.TestSuite()
    suite.addTests(test_server.suite())
    suite.addTests(test_database.suite())
    suite.addTests(test_dataset.suite())
    suite.addTest(test_filter.suite())
    suite.addTest(test_attribute.suite())
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
