import pprint
import random

from django.core.management.base import BaseCommand
from django.db import connection

from ventas.models import *

def not_id(array):
    return [x for x in array if x != 'id']

class Command(BaseCommand):
    args = '<a>'
    def handle(self, *args, **options):
        years = self.generate_times()
        countries = self.generate_branches()
        categories = self.generate_products(12000, 6, 3)

        if not args:
            self.make_dimension_records(years, countries, categories)
        else:
            self.make_facts_records(years, countries, categories)

    def make_facts_records(self, years, countries, categories):
        counter = 1
        costo = 0
        total = 0
        records = []
        cursor = connection.cursor()
        cursor.execute('SET autocommit = 1')

        for year in years:
            for month in years[year]:
                for day in years[year][month]:
                    for country in countries:
                        for city in countries[country]:
                            cursor.executemany(
                                """INSERT INTO ventas_venta (producto_id, tiempo_id, sucursal_id, costo) 
                                    VALUES (%s, %s, %s, %s)""", records
                                )
                            records = []
                            print counter
                            for branch in countries[country][city]:
                                for cat in categories:
                                    for subcat in categories[cat]:
                                        for product in categories[cat][subcat]:
                                            costo = random.random() * 10
                                            total += costo
                                            records.append((
                                                    categories[cat][subcat][product],
                                                    years[year][month][day],
                                                    countries[country][city][branch],
                                                    costo
                                                    ))
                                            counter += 1
                                SucursalDia.objects.create(
                                    sucursal_id=countries[country][city][branch],
                                    tiempo_id=years[year][month][day],
                                    total=total
                                    )
                                total = 0

    def make_dimension_records(self, years, countries, categories):
        records = []
        for year in years:
            for month in years[year]:
                for day in years[year][month]:
                    records.append(Tiempo(
                            pk=years[year][month][day],
                            dia=day,
                            mes=month,
                            anio=year
                            ))
        Tiempo.objects.bulk_create(records)

        records = []
        for country in countries:
            new_country = Pais.objects.create(nombre=country)
            for city in countries[country]:
                new_city = Ciudad.objects.create(nombre=city, pais=new_country)
                for branch in countries[country][city]:
                    records.append(Sucursal(
                            pk=countries[country][city][branch],
                            ciudad=new_city
                            ))
        Sucursal.objects.bulk_create(records)

        records = []
        for cat in categories:
            new_category = Categoria.objects.create(nombre=cat)
            for subcat in categories[cat]:
                new_subcat = SubCategoria.objects.create(
                    nombre=subcat,
                    categoria=new_category)
                for product in categories[cat][subcat]:
                    records.append(Producto(
                            pk=categories[cat][subcat][product],
                            subcategoria=new_subcat
                            ))
        Producto.objects.bulk_create(records)


    def generate_times(self):
        years = {
            2011: {},
            2012: {},
            2013: {}
            }

        counter = 1

        for key in years.keys():
            for i in range(12):
                years[key][i+1] = {}

                if i+1 == 2:
                    for j in range(28):
                        years[key][i+1][j+1] = counter
                        counter += 1
                elif i+1 in [4, 6, 9, 11]:
                    for j in range(30):
                        years[key][i+1][j+1] = counter
                        counter += 1
                else:
                    for j in range(31):
                        years[key][i+1][j+1] = counter
                        counter += 1

        return years


    def generate_branches(self):
        countries = {
            'peru': {
                'arequipa': {},
                'cusco': {},
                'ica': {},
                'juliaca': {},
                'lima': {},
                'tacna': {}
                },
            'chile': {
                'arica': {},
                'calama': {},
                'antofagasta': {},
                'santiago': {},
                'valparaiso': {},
                'copiapo': {}
                },
            'argentina': {
                'cordoba': {},
                'corrientes': {},
                'jujuy': {},
                'mendoza': {},
                'tucuman': {},
                'neuquen': {}
                },
            'bolivia': {
                'cochabamba': {},
                'oruro': {},
                'sucre': {},
                'tarija': {},
                'montero': {},
                'trinidad': {}
                },
            'colombia': {
                'bogota': {},
                'medellin': {},
                'cali': {},
                'barranquilla': {},
                'cartagena': {},
                'cucuta': {}
                },
            }

        counter = 1

        for country in countries.keys():
            for city in countries[country].keys():
                countries[country][city]['sucursal%s' % counter] = counter
                counter += 1

        return countries

    def generate_products(self, total, subcats, cats):
        categories = {}

        counter = 1

        for i in range(cats):
            cat_idx = 'cat%s' % (i+1)
            categories[cat_idx] = {}
            for j in range(subcats):
                subcat_idx = 'cat%s.%s' % (i+1, j+1)
                categories[cat_idx][subcat_idx] = {}
                for k in range(total/(cats*subcats)):
                    prod_idx = 'prod%s.%s.%s' % (i+1, j+1, k+1)
                    categories[cat_idx][subcat_idx][prod_idx] = counter
                    counter += 1

        for k in range(total % (cats*subcats)):
            subcat_idx = 'cat%s.%s' % (cats, subcats)
            prod_idx = 'prod%s.%s.%s' % (cats, subcats, (total/(cats*subcats)) + k+1)
            categories[cat_idx][subcat_idx][prod_idx] = counter
            counter += 1

        return categories
