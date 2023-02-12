# Тестовое задание для academy.infotecs.ru

Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять из географической базы данных GeoNames, по [ссылке](http://download.geonames.org/export/dump/RU.zip).
[Описание](http://download.geonames.org/export/dump/readme.txt) формата данных.

## Метод принимает идентификатор geonameid и возвращает информацию о городе.
`GET api/cities` вернёт информацию о городе.
### Пример запроса
`GET api/cities/569999`
### Ответ
Успешный ответ приходит с кодом `200 OK` и содержит тело:
```json
{
     "message": null,
     "data": {
          "geo_name_id": 569999,
          "name": "Chandar",
          "ascii_name": "Chandar",
          "alternate_names": [
               "Chandar",
               "Tsjandar",
               "Чандар"
          ],
          "latitude": 55.29917,
          "longitude": 56.71417,
          "feature_class": "P",
          "feature_code": "PPL",
          "country_code": "RU",
          "cc2": null,
          "admin1_code": "08",
          "admin2_code": null,
          "admin3_code": null,
          "admin4_code": null,
          "population": 0,
          "elevation": null,
          "dem": 105,
          "timezone": "Asia/Yekaterinburg",
          "modification_date": "2012-01-17"
     }
}
```


## Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией.
`GET api/cities` возвращает список городов с их информацией.
### Параметры:
* `page` – номер страницы
* `rows` – количество результатов на странице
### Пример запроса
`GET api/cities/?page=10&rows=3`
### Ответ
Успешный ответ приходит с кодом `200 OK` и содержит тело:
```json
{
     "message": null,
     "total": 366931,
     "data": [
          {
               "geo_name_id": 451774,
               "name": "Yakovlevo",
               "ascii_name": "Yakovlevo",
               "alternate_names": [],
               "latitude": 57.3122,
               "longitude": 34.12509,
               "feature_class": "P",
               "feature_code": "PPL",
               "country_code": "RU",
               "cc2": null,
               "admin1_code": "77",
               "admin2_code": null,
               "admin3_code": null,
               "admin4_code": null,
               "population": 0,
               "elevation": null,
               "dem": 280,
               "timezone": "Europe/Moscow",
               "modification_date": "2011-07-09"
          },
          {
               "geo_name_id": 451775,
               "name": "Yakimovo",
               "ascii_name": "Yakimovo",
               "alternate_names": [],
               "latitude": 57.14907,
               "longitude": 34.60264,
               "feature_class": "P",
               "feature_code": "PPL",
               "country_code": "RU",
               "cc2": null,
               "admin1_code": "77",
               "admin2_code": null,
               "admin3_code": null,
               "admin4_code": null,
               "population": 0,
               "elevation": null,
               "dem": 193,
               "timezone": "Europe/Moscow",
               "modification_date": "2011-07-09"
          },
          {
               "geo_name_id": 451776,
               "name": "Vysokoye",
               "ascii_name": "Vysokoye",
               "alternate_names": [],
               "latitude": 56.98226,
               "longitude": 34.43519,
               "feature_class": "P",
               "feature_code": "PPL",
               "country_code": "RU",
               "cc2": null,
               "admin1_code": "77",
               "admin2_code": null,
               "admin3_code": null,
               "admin4_code": null,
               "population": 0,
               "elevation": null,
               "dem": 202,
               "timezone": "Europe/Moscow",
               "modification_date": "2011-07-09"
          }
     ]
}
```


## Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также какой из них расположен севернее и одинаковая ли у них временная зона и на сколько часов они различаются.
###### Когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением; если население совпадает, брать первый попавшийся.
`GET api/v1/cities`
### Пример запроса
`GET /api/cities/молчаново&москва`
### Ответ
Успешный ответ приходит с кодом `200 OK` и содержит тело:
```json
{
     "message": null,
     "same_timezones": false,
     "time_difference_in_hours": 3.0,
     "more_northerly_geo_object": "Molchanovo",
     "cities_info": [
          {
               "geo_name_id": 1498493,
               "name": "Molchanovo",
               "ascii_name": "Molchanovo",
               "alternate_names": [
                    "Molchanovo",
                    "Moltsjanovo",
                    "Молчаново"
               ],
               "latitude": 57.58167,
               "longitude": 83.76917,
               "feature_class": "P",
               "feature_code": "PPL",
               "country_code": "RU",
               "cc2": null,
               "admin1_code": "75",
               "admin2_code": null,
               "admin3_code": null,
               "admin4_code": null,
               "population": 6109,
               "elevation": null,
               "dem": 104,
               "timezone": "Asia/Tomsk",
               "modification_date": "2012-01-17"
          },
          {
               "geo_name_id": 524894,
               "name": "Moskva",
               "ascii_name": "Moskva",
               "alternate_names": [
                    "Maskva",
                    "Moscou",
                    "Moscow",
                    "Moscu",
                    "Moscú",
                    "Moskau",
                    "Moskou",
                    "Moskovu",
                    "Moskva",
                    "Məskeu",
                    "Москва",
                    "Мәскеу"
               ],
               "latitude": 55.76167,
               "longitude": 37.60667,
               "feature_class": "A",
               "feature_code": "ADM1",
               "country_code": "RU",
               "cc2": null,
               "admin1_code": "48",
               "admin2_code": null,
               "admin3_code": null,
               "admin4_code": null,
               "population": 13010112,
               "elevation": null,
               "dem": 161,
               "timezone": "Europe/Moscow",
               "modification_date": "2023-01-12"
          }
     ]
}
```



## Метод принимает часть названия города и возвращает подсказку с возможными вариантами продолжений.
`GET /api/cities/search`
### Пример запроса
`GET api/cities/search/toms`
### Ответ
Успешный ответ приходит с кодом `200 OK` и содержит тело:
```json
{
     "message": null,
     "number_of_cities_found": 27,
     "data": [
          "Tomsk",
          "Tomsha",
          "Tomsyu",
          "Tomsino",
          "Tomskiy",
          "Tomskaya",
          "Tomskoye",
          "Tomsharovo",
          "Tomsk Oblast",
          "Ozero Tomsino",
          "Gora Tomskaya",
          "Tomskiy Rayon",
          "Ostrov Tomskiy",
          "Tomskiy Khutor",
          "Ozero Tomskoye",
          "Tomskaya Tamozhnya",
          "Duma Goroda Tomska",
          "Urochishche Tomshina",
          "Meriya Goroda Tomska",
          "Tomskiy Oblastnoy Sud",
          "Ozero Maloye Tomskoye",
          "Stantsiya Tomsk Vtoroy",
          "Stantsiya Tomsk Pervyy",
          "Tomsk Bogashevo Airport",
          "Ozero Bol’shoye Tomskoye",
          "Stantsiya Tomsk-Severnyy",
          "Tomsko-Obskaya Lesnaya Dacha"
     ]
}
```