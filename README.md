В переменных окружения (ENV) надо указать API токен бота

`TELEGRAM_API_TOKEN='API_токен_бота'`

Работа с Docker: 
```
docker build -t gymbot ./
docker run -d --name gym -v /local_project_path/db:/home/db gymbot
```
где:
``` 
`local_project_path`- локальная дерриктория с вашим проектом
`db/training_plan.db` - расположение SQLite базы в папке проекта
```
Чтобы войти в работающий контейнер:
```
docker exec -ti gym bash
```
Войти в контейнере в SQL шелл:
```
docker exec -ti gym bash
sqlite3 /home/db/training_plan.db   
```