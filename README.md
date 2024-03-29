[Barbara Agena](http://lattes.cnpq.br/3888793516541327), [Insper](https://www.insper.edu.br/), 2022.

<p align="center">
  <img src="notes/static/notes/image/logo-getit.png" alt="Get-it" width="256">
</p>
<h1 align="center">
  Get-it
</h1>
<p align="center">
  <i>Like the Post-it, but with another verb</i>
</p>

> As múltiplas Tags de uma nota podem ser editadas e removidas alterando as notas pertencentes. Tudo acontece automaticamente durante as requisições assíncronas do aplicativo. Além disso foi adicionada uma página de erro 404 e todas as páginas são responsivas. Para tanto, o projeto foi desenvolvido para atingir conceito A+.

## See it working
[evening-river-06330.herokuapp.com](https://evening-river-06330.herokuapp.com/)

## Start database
```bash
$ docker run --rm --name pg-docker -e POSTGRES_PASSWORD=password -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data postgres
```

```bash
$ sudo -u postgres psql
```

```sql
CREATE USER getituser WITH PASSWORD 'password';
ALTER ROLE getituser SET client_encoding TO 'utf8';
ALTER ROLE getituser SET default_transaction_isolation TO 'read committed';
ALTER ROLE getituser SET timezone TO 'UTC';
CREATE DATABASE getit WITH OWNER=getituser;
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
