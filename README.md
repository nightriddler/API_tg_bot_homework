# Телеграм-бот (ассистент)
Бот обращается к API сервиса Практикум.Домашка, узнает, взята ли домашка в ревью, проверена ли она, провалена или принята и отправляет результат в Телеграм-чат:

- При взятии работы ревьюером на проверку - ```'Ваша работа <название_работы> проходит ревью'```
- После проверки работу вернули для исправления - ```'У вас проверили работу "<название_работы>"! К сожалению в работе нашлись ошибки.<комментарий_ревьюера>'```,
- Работа принята - ```'У вас проверили работу "<название_работы>"! Ревьюеру всё понравилось, можно приступать к следующему уроку.<комментарий_ревьюера>'```

Запросы к серверу осуществляются каждые 5 минут.

Логгирование реализовано в терминал:
- В момент своего запуска (уровень DEBUG)
- Каждую отправку сообщения (уровень INFO) 
- Отправка сообщения уровня ERROR  в Телеграм

Для работы необходимо в корневой директории создать файл .env со следующими данными:

```
PRAKTIKUM_TOKEN=<токен_API_Практикум.Домашка>
TELEGRAM_TOKEN=<токен_вашего_бота>
TELEGRAM_CHAT_ID=<ID_вашего_аккаунта_в_Телеграм>
```

API домашки доступно по адресу: https://praktikum.yandex.ru/api/user_api/homework_statuses/.
Для успешного запроса нужно:
- В заголовке запроса передать токен авторизации ```Authorization: OAuth <token>```
- передать GET-параметр from_date.
Токен можно получить по адресу: https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.

Мини-документация к API сервиса Практикум.Домашка:
- API возвращает изменение статуса домашки за определённый интервал времени.
- Если статус домашки изменился за этот интервал времени, то в ответ придут данные в формате JSON.
- Интервал задаётся от времени, указанного в параметре from_date, до текущего момента. Время передаётся в формате Unix time (оно вернётся в ключе current_date, его можно использовать как начало интервала в следующем запросе).

В ответ на запрос API Практикум.Домашка пришлёт список домашних работ, статус которых изменился за запрошенный период:

```
{
   "homeworks":[
      {
         "id":123,
         "status":"rejected",
         "homework_name":"username__hw_python_oop.zip",
         "reviewer_comment":"Код не по PEP8, нужно исправить",
         "date_updated":"2020-02-11T16:42:47Z",
         "lesson_name":"Итоговый проект"
      },
      {
         "id":124,
         "status":"approved",
         "homework_name":"username__hw_python_oop.zip",
         "reviewer_comment":"Всё нравится",
         "date_updated":"2020-02-13T14:40:57Z",
         "lesson_name":"Итоговый проект"
      }
   ],
   "current_date":1581604970
}
```
