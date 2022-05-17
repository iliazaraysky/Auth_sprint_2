# Проектная работа 7 спринта

Упростите регистрацию и аутентификацию пользователей в Auth-сервисе, добавив вход через социальные сервисы. Список сервисов выбирайте исходя из целевой аудитории онлайн-кинотеатра — подумайте, какими социальными сервисами они пользуются. Например, использовать [OAuth от Github](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps){target="_blank"} — не самая удачная идея. Ваши пользователи не разработчики и вряд ли имеют аккаунт на Github. А вот добавить Twitter, Facebook, VK, Google, Yandex или Mail будет хорошей идеей.

Вам не нужно делать фронтенд в этой задаче и реализовывать собственный сервер OAuth. Нужно реализовать протокол со стороны потребителя.

Информация по OAuth у разных поставщиков данных: 

- [Twitter](https://developer.twitter.com/en/docs/authentication/overview){target="_blank"},
- [Facebook](https://developers.facebook.com/docs/facebook-login/){target="_blank"},
- [VK](https://vk.com/dev/access_token){target="_blank"},
- [Google](https://developers.google.com/identity/protocols/oauth2){target="_blank"},
- [Yandex](https://yandex.ru/dev/oauth/?turbo=true){target="_blank"},
- [Mail](https://api.mail.ru/docs/guides/oauth/){target="_blank"}.


## Ссылка на репозиторий:

https://github.com/iliazaraysky/Auth_sprint_2

## API для сайта и личного кабинета

- регистрация пользователя;
- вход пользователя в аккаунт (обмен логина и пароля на пару токенов: JWT-access токен и refresh токен); 
- обновление access-токена;
- выход пользователя из аккаунта;
- изменение логина или пароля ;
- получение пользователем своей истории входов в аккаунт;

## API для управления доступами

- CRUD для управления ролями:
  - создание роли,
  - удаление роли,
  - изменение роли,
  - просмотр всех ролей.
- назначить пользователю роль;
- отобрать у пользователя роль;
- метод для проверки наличия прав у пользователя. 


# Запуск проекта
Находясь в директории **Auth_sprint_2**, запускаем Docker:
```
sudo docker-compose -f docker-compose.yml up --build
```

## Супер пользователь
После запуска проекта, супер пользователь создается автоматически.
```
login: admin
password: password123
```

## Команда создания супер пользователя

Находясь в корне проекта набрать:
```
flask createsuperuser admin password123
```

## Документация доступна по адресу:

```
http://localhost/apidocs/
```

## JAEGER UI доступен по адресу:
```
http://localhost:16686/
```

## Проверить OAuth можно из браузера по адресу:
```
http://localhost:5000/auth/v1/google/login
```
***Если включен Nginx. Не работает без реального домена**

## Взаимодействие между сервисами
В AsyncApi/fastapi/src/main.py добавлена middleware функция, которая прежде чем
отдавать контент, ходит в Auth сервис, проверять токен пользователя

FastApi не отдаст данные без авторизации по ключу
Алгоритм действий следующий:
1. Делаем GET запрос по адресу http://127.0.0.1/api/v1/films
2. Получаем 401 ошибку
3. Регистрируемся по адресу http://127.0.0.1/auth/v1/registration
```
# POST запрос
{
    "login": "username",
    "password": "password123"
}
```
4. Заходим в аккаунт по адресу http://127.0.0.1/auth/v1/login
```
# POST запрос
{
    "login": "username",
    "password": "password123"
}
```
5. Получаем access_token, и уже с ним успешно получаем данные от FastApi http://127.0.0.1/api/v1/films
