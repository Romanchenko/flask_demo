# Flask Demo

В директории `sample` лежит небольшой пример с jinja, без фласка и прочего, просто чистые шаблоны.

В директории `back` содержится наш мини-твиттер. Вы можете сбилдить образ и запустить его:

```shell
docker build . -t my_name/my_flask_app
docker run -p 5001:5000 apollin/some-flask-app
```
После выполнения скрипта приложение будет доступно на `127.0.0.1:5001`.

Чтобы выбрать другой порт, поменяйте в аргументе `-p` 5001 на нужный незанятый порт.