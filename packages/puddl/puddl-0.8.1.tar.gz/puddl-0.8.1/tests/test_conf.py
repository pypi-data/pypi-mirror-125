import unittest


class ConfTest(unittest.TestCase):

    def test_empty_env(self):
        import os
        from puddl.db.alchemy import DBConfig
        for k in DBConfig.__slots__:
            if k in os.environ:
                del os.environ[k]
        x = DBConfig('sunrise')
        self.assertTrue(x is not None)
