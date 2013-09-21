from django.db import models

class Tiempo(models.Model):
    dia = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    anio = models.PositiveIntegerField()

class Categoria(models.Model):
    nombre = models.CharField(max_length=256)

class SubCategoria(models.Model):
    nombre = models.CharField(max_length=256)
    categoria = models.ForeignKey(Categoria)

class Producto(models.Model):
    nombre = models.CharField(max_length=256)
    subcategoria = models.ForeignKey(SubCategoria)

class Pais(models.Model):
    nombre = models.CharField(max_length=256)

class Ciudad(models.Model):
    nombre = models.CharField(max_length=256)
    pais = models.ForeignKey(Pais)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=256)
    ciudad = models.ForeignKey(Ciudad)

class Venta(models.Model):
    producto = models.ForeignKey(Producto)
    tiempo = models.ForeignKey(Tiempo)
    sucursal = models.ForeignKey(Sucursal)

    costo = models.FloatField()

class SucursalDia(models.Model):
    sucursal = models.ForeignKey(Sucursal)
    tiempo = models.ForeignKey(Tiempo)

    total = models.FloatField()
