import unittest

from puddl.db.alchemy import App


class FooTest(unittest.TestCase):
    def test_foo(self):
        import psycopg2.errorcodes
        from sqlalchemy.exc import ProgrammingError

        app = App('psycoerror')

        try:
            app.engine.execute('CREATE TABLE foo (x INT)')
            app.engine.execute('CREATE TABLE foo (x INT)')
            self.fail('should have raised')
        except ProgrammingError as e:
            if e.orig.pgcode == psycopg2.errorcodes.DUPLICATE_TABLE:
                self.assertTrue(True, "jup, it's a duplicate - as expected'")
            else:
                self.fail(e)
