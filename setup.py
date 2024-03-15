from setuptools import setup, find_packages


setup(
    name='vanuatuvoices',
    version='0.0',
    description='vanuatuvoices',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pyclts>=3.1.1',
        'clld>=11.0.1',
        'cldfbench>=1.14.0',
        'clld-glottologfamily-plugin>=4.0',
        'clld-audio-plugin>=1.0',
        'pyglottolog>=3.12.0',
        'clldmpg>=4.3.0',

],
extras_require={
        'dev': ['flake8', 'waitress', 'psycopg2'],
        'test': [
            'pytest>=7.4.2',
            'pytest-clld>=1.2',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="vanuatuvoices",
    message_extractors={'vanuatuvoices': [
        ('**.py', 'python', None),
        ('**.mako', 'mako', {'encoding': 'utf8'}),
        ('web/static/**', 'ignore', None)]},
    entry_points="""\
    [paste.app_factory]
    main = vanuatuvoices:main
""")
