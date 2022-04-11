[Barbara Agena](http://lattes.cnpq.br/3888793516541327), [Insper](https://www.insper.edu.br/), 2022.

<p align="center">
  <img src="public/image/logo-getit.png" alt="Get-it" width="256">
</p>
<h1 align="center">
  Get-it
</h1>
<p align="center">
  <i>Like the Post-it, but with another verb</i>
</p>


## Start database
```bash
$ docker run --rm --name pg-docker -e POSTGRES_PASSWORD=getitsenha -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
```

```bash
$ psql -h localhost -U postgres
```

```sql
CREATE DATABASE getit;
CREATE USER getituser WITH PASSWORD 'getitsenha';
ALTER ROLE getituser SET client_encoding TO 'utf8';
ALTER ROLE getituser SET default_transaction_isolation TO 'read committed';
ALTER ROLE getituser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE getit TO getituser;
\q
```

## Start application
```bash
$ python manage.py runserver
Application running on http://localhost:8000
```

## License
This project is (not yet) [MIT licensed](https://www.insper.edu.br/).