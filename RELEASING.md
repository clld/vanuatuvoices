# Releasing the Vanuatu Voices clld app

```shell
git clone https://github.com/clld/vanuatuvoices
git clone --branch v1.6.0 --depth 1 https://github.com/lexibank/vanuatuvoices vanuatuvoices-cldf
git clone --branch v2.3.1 --depth 1 https://github.com/cldf-clts/clts
cd vanuatuvoices
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../vanuatuvoices-cldf/cldf/cldf-metadata.json --clts ../../cldf-clts/clts-data
```

```shell
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump: 
```shell
pg_dump -xO --compress gzip:9 vanuatuvoices > vanuatuvoices.sql.gz
```

