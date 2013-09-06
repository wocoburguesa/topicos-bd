import pprint

from ventas.models import *

def generate_times():
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

    years['id'] = None

    return years


def generate_branches():
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

def generate_products(total, subcats, cats):
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

def make_records():
    years = generate_times()
    countries = generate_branches()
    categories = generate_products(12000, 6, 3)

    for year in years.keys():
        if year != 'id':
            print year

if __name__ == '__main__':
    print 'hola'
