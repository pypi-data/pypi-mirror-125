from .repo2rows import iter_records, get_df


def test_records(here):
    records = list(iter_records(here))
    assert len(records) > 0


def test_get_df(here):
    df = get_df(here)
    print(df.astype({'dt': 'str'}).dtypes)
