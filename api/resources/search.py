from flask import jsonify
from flask_restful import Resource, abort

from api.common import *


class PartCityNameSearch(Resource):
    @staticmethod
    def get(part_city_name):
        """
        Метод принимает часть названия города part_city_name.
        Вызывается функция для поиска названий географических объектов, содержащих полученную строку.
        Если поиск не дал результатов, то формируется ответ со статус-кодом 404 NOT FOUND и json файлом.
        {
            "message": "Geographical objects with part names were not found.",
            "number_of_cities_found": null,
            "data": []
        }
        Если Результат поиска содержит результаты, то формируется ответ,
        добавляется количество найденных названий географических объектов,
        а результаты поиска сортируются по длине названий.
        Метод возвращает ответ со статус-кодом 200 ОК и json файл.
        :param part_city_name:
        :return:
        """
        response = {
            "message": None,
            "number_of_cities_found": None,
            "data": []
        }

        search = part_city_name_search(part_city_name)

        if not search:
            response['message'] = "Geographical objects with part names were not found."
            response["http_status_code"] = 404
            abort(**response)

        response['number_of_cities_found'] = len(search)
        response['data'].extend(search)
        response['data'].sort(key=len)
        return jsonify(response)
