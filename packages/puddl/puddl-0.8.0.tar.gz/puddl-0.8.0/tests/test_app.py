import unittest

from puddl.db.alchemy import App


class AppTest(unittest.TestCase):
    def test_create_and_connect(self):
        app = App('sunrise')
        app.engine.execute('SELECT 1').first()

        app2 = App('sunrise')
        app2.engine.execute('SELECT 1').first()

    def test_df_dump(self):
        import logging
        logging.getLogger('puddl.db.alchemy').setLevel(logging.DEBUG)
        import pandas as pd
        app = App('sunrise')
        df = pd.DataFrame({'foo': [1, 2], 'bar': [5, 6]})
        app.df_dump(df, 'test_df_dump')
