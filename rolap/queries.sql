-- totales por sucursal
select CONCAT('sucursal ', s.id) as sucursal, t.dia, t.mes, t.anio, a.total from ventas_sucursal s, ventas_tiempo t, ventas_sucursaldia a where a.sucursal_id = s.id AND a.tiempo_id = t.id;

-- totales por dia
select t.dia, t.mes, t.anio, sum(a.total) from ventas_tiempo t, ventas_sucursaldia a where a.tiempo_id = t.id group by a.tiempo_id;

-- totales por mes
select mes, anio, sum(total) from (select t.dia, t.mes, t.anio, sum(a.total) as total from ventas_tiempo t, ventas_sucursaldia a where a.tiempo_id = t.id group by a.tiempo_id) as bolas group by mes, anio order by anio, mes;

-- totales por anio
select anio, sum(total) from (select t.dia, t.mes, t.anio, sum(a.total) as total from ventas_tiempo t, ventas_sucursaldia a where a.tiempo_id = t.id group by a.tiempo_id) as bolas group by anio order by anio;

-- total por sucursal especifica y dia especifico
select * from ventas_sucursaldia where tiempo_id=(select id from ventas_tiempo where dia=1 AND mes=1 AND anio=2011) AND sucursal_id=(select id from ventas_sucursal where ciudad_id = (select id from ventas_ciudad where nombre='arequipa'));

-- total por sucursal especifica y mes especifico
select c.nombre, sum(total)  from ventas_sucursaldia a, ventas_ciudad c where tiempo_id IN (select id from ventas_tiempo where mes=1 AND anio=2011) AND sucursal_id=(select id from ventas_sucursal where ciudad_id = (select id from ventas_ciudad where nombre='arequipa')) AND c.id=sucursal_id ;

-- total por sucursal especifica y anio especifico
select c.nombre, sum(total)  from ventas_sucursaldia a, ventas_ciudad c where tiempo_id IN (select id from ventas_tiempo where anio=2011) AND sucursal_id=(select id from ventas_sucursal where ciudad_id = (select id from ventas_ciudad where nombre='arequipa')) AND c.id=sucursal_id ;

-- totales por pais
select p.nombre, sum(total) from ventas_sucursaldia a, ventas_pais p, ventas_ciudad c, ventas_sucursal s where s.id = a.sucursal_id and c.id = s.ciudad_id and p.id = c.pais_id group by p.nombre;

-- totales por ciudad
select c.nombre, sum(total) from ventas_sucursaldia a, ventas_ciudad c, ventas_sucursal s where s.id = a.sucursal_id and c.id = s.ciudad_id group by c.nombre;
