# CuruenoPormaWarbot

Repositorio con el código para el intento de warbot para el curueño 
condado, acompañadme en esta terrible epopeya de la mala programación.

## How to run?
1. Duplicate the [.env.template](.env.template) file and rename it as `.env`.

### Using docker dev env (Recommended)
2. Run `make dev`
3. Profit!

When it finishes you will have deployed:
- [Adminer](https://www.adminer.org/) on port `ADMINER_PORT`
- [MySQL](https://www.mysql.com/) on port 3306
- The CuruenoPormaWarbot.
 
### Locally
You need to have a MySQL instance running, make sure you update the `.env`
variables accordingly!

2. Install poetry if you haven't already.
3. Run `poetry install`
4. Run `python main.py`
5. Profit!

## To Dos
- ![TODO.md](TODO.md)
