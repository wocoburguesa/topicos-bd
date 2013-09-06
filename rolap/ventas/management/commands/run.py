import pprint
import random

from django.core.management.base import NoArgsCommand

from ventas.models import *

def not_id(array):
    return [x for x in array if x != 'id']

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        years = self.generate_times()
        countries = self.generate_branches()
        categories = self.generate_products(18, 6, 3)
        dummies = self.generate_dummies()

        self.process_dates(years, countries, categories, dummies)

    def process_dates(self, years, countries, categories, dummies):
        counter = 0
        for year in not_id(years.keys()):
            total_year = 0
            for month in [x+1 for x in range(12)]:
                total_month = 0
                for day in not_id(years[year][month].keys()):
                    print 'Processing day: %s/%s/%s' % (month, day, year)
                    new_day = Tiempo(
                        dia=day,
                        mes=month,
                        anio=year
                        )
                    new_day.save()
#                    years[year][month][day]['id'] = new_day.id

                    total_day, counter = self.process_countries(countries, categories, dummies, new_day.id, counter)
                    total_month += total_day

                new_day = Tiempo(
                    dia=0,
                    mes=month,
                    anio=year
                    )
                new_day.save()
                new_sale = Venta(
                    producto_id=dummies['product'],
                    tiempo=new_day,
                    sucursal_id=dummies['branch'],
                    costo=total_month
                    )
                new_sale.save()
                total_year += total_month

            new_day = Tiempo(
                dia=0,
                mes=0,
                anio=year
                )
            new_day.save()
            new_sale = Venta(
                producto_id=dummies['product'],
                tiempo=new_day,
                sucursal_id=dummies['branch'],
                costo=total_year
                )
            new_sale.save()

    def process_countries(self, countries, categories, dummies, new_day, counter):
        total = 0
        for country in not_id(countries.keys()):
            new_country = Pais(
                nombre=country
                )
            new_country.save()
#            countries[country]['id'] = new_country.id

            total_country = 0

            for city in not_id(countries[country].keys()):
                new_city = Ciudad(
                    nombre=city,
                    pais_id=new_country.id
                    )
                new_city.save()
#                countries[country][city]['id'] = new_city.id

                total_city = 0

                for branch in not_id(countries[country][city].keys()):
                    print 'Processing branch: %s->%s->%s' % (
                        country, city, branch
                        )
                    new_branch = Sucursal(
                        nombre=branch,
                        ciudad_id=new_city.id
                        )
                    new_branch.save()
#                    countries[country][city][branch]['id'] = new_branch.id

                    total_branch, counter = self.process_categories(categories, new_day, new_branch.id, counter)
                    total_city += total_branch

                    new_sale = Venta(
                        producto_id=dummies['product'],
                        tiempo_id=new_day,
                        sucursal_id=new_branch.id,
                        costo=total_branch
                        )
                    new_sale.save()

                new_branch = Sucursal(
                    nombre='TOTAL_CITY',
                    ciudad_id=new_city.id
                    )
                new_branch.save()
                new_sale = Venta(
                    producto_id=dummies['product'],
                    tiempo_id=new_day,
                    sucursal_id=new_branch.id,
                    costo=total_city
                    )
                new_sale.save()
                total_country += total_city

            new_city = Ciudad(
                nombre='TOTAL_COUNTRY',
                pais_id=new_country.id
                )
            new_city.save()
            new_branch = Sucursal(
                nombre='NONE',
                ciudad_id=new_city.id
                )
            new_branch.save()
            new_sale = Venta(
                producto_id=dummies['product'],
                tiempo_id=new_day,
                sucursal_id=new_branch.id,
                costo=total_country
                )
            new_sale.save()
            total += total_country

        return (total, counter)

    def process_categories(self, categories, new_day, new_branch, counter):
        total = 0
        for cat in not_id(categories.keys()):
            print 'Processing cat: %s' % cat
            new_category = Categoria(
                nombre=cat
                )
            new_category.save()
#            categories[cat]['id'] = new_category.id

            total_cat = 0

            for subcat in not_id(categories[cat].keys()):
#                print 'Processing subcat: %s' % subcat
                new_subcat = SubCategoria(
                    nombre=subcat,
                    categoria_id=new_category.id
                    )
                new_subcat.save()
#                categories[cat][subcat]['id'] = new_subcat.id

                total_subcat = 0

                new_sales = []
                for product in not_id(categories[cat][subcat].keys()):
                    counter += 1
                    new_product = Producto(
                        nombre=product,
                        subcategoria_id=new_subcat.id
                        )
                    new_product.save()
#                    categories[cat][subcat][product]['id'] = new_product.id

                    cost = random.random() * 100
                    total_subcat += cost
                    new_sales.append(Venta(
                        producto_id=new_product.id,
                        tiempo_id=new_day,
                        sucursal_id=new_branch,
                        costo=cost
                        ))

                Venta.objects.bulk_create(new_sales)

                new_product = Producto(
                    nombre='TOTAL_SUBCAT',
                    subcategoria_id=new_subcat.id
                    )
                new_product.save()

                new_sale = Venta(
                    producto_id=new_product.id,
                    tiempo_id=new_day,
                    sucursal_id=new_branch,
                    costo=total_subcat
                    )
                new_sale.save()
                total_cat += total_subcat

            new_subcat = SubCategoria(
                nombre='TOTAL_CAT',
                categoria_id=new_category.id
                )
            new_subcat.save()
            new_product = Producto(
                nombre='NONE',
                subcategoria_id=new_subcat.id
                )
            new_product.save()

            new_sale = Venta(
                producto_id=new_product.id,
                tiempo_id=new_day,
                sucursal_id=new_branch,
                costo=total_cat
                )
            new_sale.save()
            total += total_cat
            print 'Done, current count: %s' % counter

        return (total, counter)

    def generate_dummies(self):
        dummy_category = Categoria(
            nombre="NONE"
            )
        dummy_category.save()
        dummy_subcat = SubCategoria(
            nombre="NONE",
            categoria=dummy_category
            )
        dummy_subcat.save()
        dummy_product = Producto(
            nombre="NONE",
            subcategoria=dummy_subcat
            )
        dummy_product.save()

        dummy_country = Pais(
            nombre="NONE"
            )
        dummy_country.save()
        dummy_city = Ciudad(
            nombre="NONE",
            pais=dummy_country
            )
        dummy_city.save()
        dummy_branch = Sucursal(
            nombre="NONE",
            ciudad=dummy_city
            )
        dummy_branch.save()

        return {
            'product': dummy_product.id,
            'branch': dummy_branch.id
            }

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

