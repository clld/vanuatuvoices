# Releasing the Vanuatu Voices clld app

```shell
git clone https://github.com/clld/vanuatuvoices
cd vanuatuvoices
pip install -e .[test]
```

```shell
clld initdb development.ini --cldf ../vanuatuvoices-cldf/cldf/cldf-metadata.json
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
pg_dump -xO vanuatuvoices > vanuatuvoices.sql
zip vanuatuvoices.sql.zip vanuatuvoices.sql
```

