import pprint

from django.core.management.base import NoArgsCommand

from ventas.models import *

def not_id(array):
    return [x for x in array if x != 'id']

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        years = self.generate_times()
        countries = self.generate_branches()
        categories = self.generate_products(12000, 6, 3)

        for year in not_id(years.keys()):
            for month in [x+1 for x in range(12)]:
                for day in not_id(years[year][month].keys()):
                    new_day, created = Tiempo.objects.get_or_create(
                        dia=day,
                        mes=month,
                        anio=year
                        )
                    years[year][month][day]['id'] = new_day.id

                    for country in not_id(countries.keys()):
                        new_country, created = Pais.objects.get_or_create(
                            nombre=country
                            )
                        countries[country]['id'] = new_country.id

                        for city in not_id(countries[country].keys()):
                            new_city, created = Ciudad.objects.get_or_create(
                                nombre=city,
                                pais=new_country
                                )
                            countries[country][city]['id'] = new_city.id

                            for branch in not_id(countries[country][city].keys()):
                                new_branch, created = Sucursal.objects.get_or_create(
                                    nombre=branch,
                                    ciudad=new_city
                                    )
                                countries[country][city][branch]['id'] = new_branch.id

                                for cat in not_id(categories.keys()):
                                    new_category, created = Categoria.objects.get_or_create(
                                        nombre=cat
                                        )
                                    categories[cat]['id'] = new_category.id

                                    for subcat in not_id(categories[cat].keys()):
                                        new_subcat, created = SubCategoria.objects.get_or_create(
                                            nombre=subcat,
                                            categoria=new_category
                                            )
                                        categories[cat][subcat]['id'] = new_subcat.id

                                        total_subcat = 0

                                        for product in not_id(categories[cat][subcat].keys()):
                                            new_product, created = Producto.objects.get_or_create(
                                                nombre=product,
                                                subcategoria=new_subcat
                                                )
                                            categories[cat][subcat][product]['id'] = new_product.id

    def generate_times(self):
        years = {
            2011: {},
            2012: {},
            2013: {}
            }

        for key in years.keys():
            for i in range(12):
                years[key][i+1] = {}

                if i+1 == 2:
                    for j in range(28):
                        years[key][i+1][j+1] = {'id': None}
                elif i+1 in [4, 6, 9, 11]:
                    for j in range(30):
                        years[key][i+1][j+1] = {'id': None}
                else:
                    for j in range(31):
                        years[key][i+1][j+1] = {'id': None}

                years[key][i+1]['id'] = None

            years[key]['id'] = None

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
                countries[country][city]['sucursal%s' % counter] = {'id': None}
                counter += 1
                countries[country][city]['id'] = None
            countries[country]['id'] = None

        return countries

    def generate_products(self, total, subcats, cats):
        categories = {}

        for i in range(cats):
            cat_idx = 'cat%s' % (i+1)
            categories[cat_idx] = {}
            for j in range(subcats):
                subcat_idx = 'cat%s.%s' % (i+1, j+1)
                categories[cat_idx][subcat_idx] = {}
                for k in range(total/(cats*subcats)):
                    prod_idx = 'prod%s.%s.%s' % (i+1, j+1, k+1)
                    categories[cat_idx][subcat_idx][prod_idx] = {'id': None}

                categories[cat_idx][subcat_idx]['id'] = None

            categories[cat_idx]['id'] = None

        return categories

