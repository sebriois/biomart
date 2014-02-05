import test_server
import test_database
import test_dataset

def suite():
    import unittest
    import doctest
    suite = unittest.TestSuite()
    suite.addTests(test_server.suite())
    suite.addTests(test_database.suite())
    suite.addTests(test_dataset.suite())
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
