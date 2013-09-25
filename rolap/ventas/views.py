import datetime
import json
import pprint

from django.http import HttpResponse
from django.core import serializers

from ventas.models import *

def sucursal_dia_s(request):
    fecha = {
        'dia': int(request.GET.get('dia', '')),
        'mes': int(request.GET.get('mes', '')),
        'anio': int(request.GET.get('anio', '')),
        }
    sucursal = {
        'ciudad': request.GET.get('ciudad', '')
        }

    tiempo = Tiempo.objects.get(dia=fecha['dia'], mes=fecha['mes'], anio=fecha['anio'])
    ciudad = Ciudad.objects.get(nombre=sucursal['ciudad'])
    sucursal_ = Sucursal.objects.get(ciudad_id=ciudad.id)

    total = SucursalDia.objects.get(sucursal_id=sucursal_.id, tiempo_id=tiempo.id)
    
    resultado = {
        'fecha': fecha,
        'sucursal': sucursal,
        'total': total.total
        }
    return HttpResponse(json.dumps(resultado), content_type="application/json")
