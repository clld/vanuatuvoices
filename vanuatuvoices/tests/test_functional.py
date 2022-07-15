import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/credits'),
        ('get_html', '/sources'),
        ('get_html', '/sources/Shimelman2019.snippet.html'),
        ('get_html', '/languages'),
        ('get_html', '/languages/Atchinorap'),
        ('get_html', '/languages/Atchinorap#ipa'),
        ('get_html', '/languages/Atchinorap?__locale__=eo'),
        ('get_dt', '/languages?iSortingCols=1&iSortCol_0=1'),
        ('get_html', '/parameters'),
        ('get_html', '/parameters/18_i'),
        ('get_html', '/values'),
        ('get_html', '/contributors'),
        ('get_html', '/contributions'),
        ('get_html', '/valuesets'),
        ('get_html', '/values/Tiraxorap-1_one-1'),
        ('get_dt', '/parameters?sSearch_2=right'),
        ('get_dt', '/values?sSearch_2=right'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)

