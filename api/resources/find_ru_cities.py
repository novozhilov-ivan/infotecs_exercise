from flask import jsonify
from flask_restful import Resource, abort

from api.common import *


class TwoRuCities(Resource):
    @staticmethod
    def get(first_ru_geo_obj, second_ru_geo_obj):
        """
        Метод принимает названия двух городов на русском языке.
        Вызывает функцию для поиска и передает названия двух городов.
        Если в полученной информации о городах не содержится ничего, то формируется ответ со статус-кодом 404 NOT FOUND
        и отправляется ответ в виде json файла
        {
             "message": "Geographical objects doesn't exist.",
             "same_timezones": null,
             "time_difference_in_hours": null,
             "more_northerly_geo_object": null,
             "cities_info": [
                  null,
                  null
             ]
        }
        Если в полученной информации о городах содержится информация только об одном городе,
        то формируется ответ со статус-кодом 400 BAD REQUEST и отправляется ответ в виде json файла
        {
             "message": "One of the geographic objects does not exist.",
             "same_timezones": null,
             "time_difference_in_hours": null,
             "more_northerly_geo_object": null,
             "cities_info": [
                  null,
                  {
                       "geo_name_id": 483893,
                       "name": "Taz",
                       "ascii_name": "Taz",
                       "alternate_names": [
                            "Taz",
                            "Таз"
                       ],
                       "latitude": 57.4391,
                       "longitude": 57.3105,
                       "feature_class": "H",
                       "feature_code": "STM",
                       "country_code": "RU",
                       "cc2": null,
                       "admin1_code": "90",
                       "admin2_code": null,
                       "admin3_code": null,
                       "admin4_code": null,
                       "population": 0,
                       "elevation": null,
                       "dem": 122,
                       "timezone": "Asia/Yekaterinburg",
                       "modification_date": "2012-01-17"
                  }
             ]
        }
        Если информация о двух городах найдена,
        то вызываются функции для сравнения временных зон и сравнения широт, найденных городов.
        Формируется словарь со всей найденной и рассчитанной информацией и отправляет в виде json файла,
        со статус_кодом 200 ОК.
        :param first_ru_geo_obj:
        :param second_ru_geo_obj:
        :return:
        """
        response = {
            "message": None,
            "same_timezones": None,
            "time_difference_in_hours": None,
            "more_northerly_geo_object": None,
            "cities_info": None
        }
        info_of_two_ru_cities = find_two_ru_cities(first_ru_geo_obj, second_ru_geo_obj)
        response['cities_info'] = info_of_two_ru_cities
        if any(info_of_two_ru_cities) is False:
            response['message'] = "Geographical objects doesn't exist."
            response['http_status_code'] = 404
            abort(**response)
        elif None in info_of_two_ru_cities:
            response['message'] = "One of the geographic objects does not exist."
            response['http_status_code'] = 400
            abort(**response)

        response['same_timezones'], response['time_difference_in_hours'] = compare_timezones(info_of_two_ru_cities)
        response['more_northerly_geo_object'] = compare_latitude(info_of_two_ru_cities)

        return jsonify(response)
