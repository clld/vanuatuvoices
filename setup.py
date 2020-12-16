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
        'clld>=7.4.1',  # >=7.0
        'cldfbench',
        'clld-glottologfamily-plugin>=4.0',
        'pyglottolog',
        'clldmpg',

],
extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'mock',
            'pytest>=5.4',
            'pytest-clld',
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
