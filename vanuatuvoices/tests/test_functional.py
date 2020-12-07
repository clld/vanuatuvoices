def test_home(app):
    app.get_html('/', status=200)
    app.get_html('/credits', status=200)

