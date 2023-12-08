-- Vista
CREATE VIEW reportes AS
SELECT rep.id,
       tr.tipo_reportante,
       rep.tipo_victima,
       rev.rango_edad,
       gi.genero_identidad,
       ge.genero_expresion,
       t.tipo_agresion,
       sa.subtipo_agresion,
       os.orientacion_sexual,
       rep.descripcion_incidente,
       rep.dia_incidente,
       rep.hora_incidente,
       e.entidad,
       c.ciudad,
       tla.lugar_agresion,
       sla.subtipo_lugar_agresion,
       rep.locacion_incidente,
       rep.reporte_previo,
       rep.reporte_previo_id,
       (
           CASE
        WHEN rep.reporte_previo_quien_id IS NULL THEN
           '-'
        ELSE
           trpq.tipo_reporte_previo_quien
        END
       ) AS reporte_previo_quien,
       rep.satisfaccion_reporte_previo,
       rep.razon_no_reporte_previo,
       ec.estado_civil,
       n.nacionalidad,
       ne.nivel_estudio,
       o.ocupacion,
       ti.tipo_ingreso,
       tss.tipo_seguridad_social,
       i.identidad,
       rep.created_at,
       rep.updated_at
FROM reportes rep
    INNER JOIN tipos_reportantes tr on tr.id = rep.tipo_reportante_id
    INNER JOIN rangos_edad_victimas rev on rev.id = rep.rango_edad_victima_id
    INNER JOIN generos_identidad gi on gi.id = rep.genero_identidad_id
    INNER JOIN generos_expresion ge on ge.id = rep.genero_expresion_id
    INNER JOIN tipos_agresor ta on ta.id = rep.tipo_agresor_id
    INNER JOIN subtipos_agresion sa on sa.id = rep.categoria_agresion_id
    INNER JOIN tipos_agresion t on t.id = sa.tipo_agresion_id
    INNER JOIN orientaciones_sexuales os on os.id = rep.orientacion_sexual_id
    INNER JOIN ciudades c on c.id = rep.ciudad_id
    INNER JOIN entidades e on e.id = c.entidad_id
    INNER JOIN subtipos_lugar_agresion sla on sla.id = rep.categoria_lugar_agresion_id
    INNER JOIN tipos_lugar_agresion tla on tla.id = sla.tipo_lugar_agresion_id
    INNER JOIN tipos_reporte_previo_quien trpq on trpq.id = rep.reporte_previo_quien_id
    INNER JOIN estados_civiles ec on ec.id = rep.estado_civil_id
    INNER JOIN nacionalidades n on n.id = rep.nacionalidad_id
    INNER JOIN niveles_estudio ne on ne.id = rep.nivel_estudio_id
    INNER JOIN ocupaciones o on o.id = rep.ocupacion_id
    INNER JOIN tipos_ingreso ti on ti.id = rep.ingreso_id
    INNER JOIN tipos_seguridad_social tss on tss.id = rep.tipo_seguridad_social_id
    INNER JOIN identidades i on i.id = rep.identidad_id;