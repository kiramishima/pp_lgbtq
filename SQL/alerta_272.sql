CREATE DATABASE alerta_272;

-- Creamos el usuario de la DB
CREATE USER dbadmin WITH PASSWORD '5V%47ñ8QoPDq';

-- Permisos
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dbadmin;

-- Creamos las extensiones extension
CREATE EXTENSION IF NOT EXISTS citext; -- Busqueda
CREATE EXTENSION IF NOT EXISTS postgis; -- PostGis

-- tipos reportantes
CREATE TABLE IF NOT EXISTS tipos_reportantes (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_reportante VARCHAR(30) NOT NULL UNIQUE CHECK ( TRIM(tipo_reportante) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);


-- tipos testigos
CREATE TABLE IF NOT EXISTS tipos_testigos (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_testigo VARCHAR(30) NOT NULL UNIQUE CHECK ( TRIM(tipo_testigo) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- rango edades victimas
CREATE TABLE IF NOT EXISTS rangos_edad_victimas (
    id SERIAL NOT NULL PRIMARY KEY,
    rango_edad VARCHAR(40) NOT NULL UNIQUE CHECK ( TRIM(rango_edad) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- identidades genero
CREATE TABLE IF NOT EXISTS generos_identidad (
    id SERIAL NOT NULL PRIMARY KEY,
    genero_identidad VARCHAR(50) NOT NULL UNIQUE CHECK ( TRIM(genero_identidad) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Orientacion sexual
CREATE TABLE IF NOT EXISTS orientaciones_sexuales (
    id SERIAL NOT NULL PRIMARY KEY,
    orientacion_sexual VARCHAR(50) NOT NULL UNIQUE CHECK ( TRIM(orientacion_sexual) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- expresion genero
CREATE TABLE IF NOT EXISTS generos_expresion (
    id SERIAL NOT NULL PRIMARY KEY,
    genero_expresion VARCHAR(50) NOT NULL UNIQUE CHECK ( TRIM(genero_expresion) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- tipos de agresores
CREATE TABLE IF NOT EXISTS tipos_agresor (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_agresor VARCHAR(100) NOT NULL UNIQUE CHECK ( TRIM(tipo_agresor) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- tipos de agresión
CREATE TABLE IF NOT EXISTS tipos_agresion (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_agresion VARCHAR(120) NOT NULL UNIQUE CHECK ( TRIM(tipo_agresion) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- subtipos de agresión
CREATE TABLE IF NOT EXISTS subtipos_agresion (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_agresion_id INT NOT NULL,
    subtipo_agresion VARCHAR(150) NOT NULL UNIQUE CHECK ( TRIM(subtipo_agresion) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT fk_tipo_agresion
        FOREIGN KEY(tipo_agresion_id) REFERENCES tipos_agresion(id)
);

-- entidades
CREATE TABLE IF NOT EXISTS entidades (
    id SERIAL NOT NULL PRIMARY KEY,
    entidad VARCHAR(50) NOT NULL UNIQUE CHECK ( TRIM(entidad) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- ciudades
CREATE TABLE IF NOT EXISTS ciudades (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    entidad_id INT NOT NULL,
    ciudad VARCHAR(50) NOT NULL CHECK (TRIM(ciudad) != ''),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT fk_entidad
        FOREIGN KEY(entidad_id) REFERENCES entidades(id)
);

-- tipos de lugar de la agresión
CREATE TABLE IF NOT EXISTS tipos_lugar_agresion (
    id SERIAL NOT NULL PRIMARY KEY,
    lugar_agresion VARCHAR(50) NOT NULL UNIQUE CHECK(TRIM(lugar_agresion) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- subtipos de lugar de la agresión
CREATE TABLE IF NOT EXISTS subtipos_lugar_agresion (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_lugar_agresion_id INT NOT NULL,
    subtipo_lugar_agresion VARCHAR(120) NOT NULL CHECK(TRIM(subtipo_lugar_agresion) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT fk_tipo_lugar_agresion
        FOREIGN KEY(tipo_lugar_agresion_id) REFERENCES tipos_lugar_agresion(id)
);

ALTER TABLE subtipos_lugar_agresion ADD CONSTRAINT uq_tipo_lugar_agresion_idx_subtipo_lugar_agresion UNIQUE (id, subtipo_lugar_agresion);

-- tipos de identidad reporte previo
CREATE TABLE IF NOT EXISTS tipos_reporte_previo_quien (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_reporte_previo_quien VARCHAR(150) NOT NULL UNIQUE CHECK(TRIM(tipo_reporte_previo_quien) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- estado_civil
CREATE TABLE IF NOT EXISTS estados_civiles (
    id SERIAL NOT NULL PRIMARY KEY,
    estado_civil VARCHAR(50) NOT NULL UNIQUE CHECK(TRIM(estado_civil) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- nacionalidad
CREATE TABLE IF NOT EXISTS nacionalidades (
    id SERIAL NOT NULL PRIMARY KEY,
    nacionalidad VARCHAR(50) NOT NULL UNIQUE CHECK(TRIM(nacionalidad) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- tipos ingresos
CREATE TABLE IF NOT EXISTS tipos_ingreso (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_ingreso VARCHAR(100) NOT NULL UNIQUE CHECK(TRIM(tipo_ingreso) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- tipos seguridad social
CREATE TABLE IF NOT EXISTS tipos_seguridad_social (
    id SERIAL NOT NULL PRIMARY KEY,
    tipo_seguridad_social VARCHAR(50) NOT NULL UNIQUE CHECK(TRIM(tipo_seguridad_social) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Antes escolaridad ahora nivel de estudios
CREATE TABLE IF NOT EXISTS niveles_estudio (
    id SERIAL NOT NULL PRIMARY KEY,
    nivel_estudio VARCHAR(50) NOT NULL CHECK ( TRIM(nivel_estudio) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Ocupación
CREATE TABLE IF NOT EXISTS ocupaciones (
    id SERIAL NOT NULL PRIMARY KEY,
    ocupacion VARCHAR(50) NOT NULL CHECK ( TRIM(ocupacion) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Identidades
CREATE TABLE IF NOT EXISTS identidades (
    id SERIAL NOT NULL PRIMARY KEY,
    identidad VARCHAR(180) NOT NULL CHECK ( TRIM(identidad) != '' ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Reportes Procesados
CREATE TABLE IF NOT EXISTS processed_reports (
    id SERIAL NOT NULL PRIMARY KEY,
    ref_report_id BIGINT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Reporte
CREATE TYPE Sexo AS ENUM ('H', 'M');

CREATE TABLE IF NOT EXISTS reportes (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    tipo_reportante_id INT NOT NULL DEFAULT 1,
    tipo_victima VARCHAR(20) NOT NULL DEFAULT 'Determinada' CHECK ( tipo_victima IN ('Determinada', 'Indeterminada') ),
    rango_edad_victima_id INT NOT NULL DEFAULT 1,
    sexo_nacimiento Sexo NOT NULL CHECK (sexo_nacimiento IN ('H', 'M') ),
    genero_identidad_id INT NOT NULL,
    genero_expresion_id INT NOT NULL,
    tipo_agresor_id INT NOT NULL,
    categoria_agresion_id INT NOT NULL,
    orientacion_sexual_id INT NOT NULL,
    descripcion_incidente TEXT NOT NULL DEFAULT 'Sin descripción',
    dia_incidente DATE NOT NULL,
    hora_incidente TIME NOT NULL,
    ciudad_id INT NOT NULL,
    categoria_lugar_agresion_id INT NOT NULL,
    locacion_incidente GEOGRAPHY NOT NULL,
    reporte_previo CHAR(2) NOT NULL DEFAULT 'No' CHECK ( reporte_previo IN ('Si', 'No') ),
    reporte_previo_id INT NULL,
    reporte_previo_quien_id INT NOT NULL,
    satisfaccion_reporte_previo DECIMAL(2, 2) NOT NULL DEFAULT 0,
    razon_no_reporte_previo TEXT NOT NULL DEFAULT 'Sin razón',
    estado_civil_id INT NOT NULL,
    nacionalidad_id INT NOT NULL,
    nivel_estudio_id INT NOT NULL,
    ocupacion_id INT NOT NULL,
    ingreso_id INT NOT NULL,
    tipo_seguridad_social_id INT NOT NULL,
    identidad_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP,
    CONSTRAINT fk_tipo_reportante_reporte
        FOREIGN KEY(tipo_reportante_id) REFERENCES tipos_reportantes(id),
    CONSTRAINT fk_rango_edad_victima_reporte
        FOREIGN KEY(rango_edad_victima_id) REFERENCES rangos_edad_victimas(id),
    CONSTRAINT fk_genero_identidad_reporte
        FOREIGN KEY(genero_identidad_id) REFERENCES generos_identidad(id),
    CONSTRAINT fk_orientacion_sexual_reporte
        FOREIGN KEY(orientacion_sexual_id) REFERENCES orientaciones_sexuales(id),
    CONSTRAINT fk_genero_expresion_reporte
        FOREIGN KEY(genero_expresion_id) REFERENCES generos_expresion(id),
    CONSTRAINT fk_tipo_agresor_reporte
        FOREIGN KEY(tipo_agresor_id) REFERENCES tipos_agresor(id),
    CONSTRAINT fk_categoria_agresion_reporte
        FOREIGN KEY(categoria_agresion_id) REFERENCES subtipos_agresion(id),
    CONSTRAINT fk_ciudad_reporte
        FOREIGN KEY(ciudad_id) REFERENCES ciudades(id),
    CONSTRAINT fk_categoria_lugar_agresion_reporte
        FOREIGN KEY(categoria_lugar_agresion_id) REFERENCES subtipos_lugar_agresion(id),
    CONSTRAINT fk_reporte_previo_reporte
        FOREIGN KEY(reporte_previo_id) REFERENCES reportes(id),
    CONSTRAINT fk_reporte_previo_quien_reporte
        FOREIGN KEY(reporte_previo_quien_id) REFERENCES tipos_reporte_previo_quien(id),
    CONSTRAINT fk_estado_civil_reporte
        FOREIGN KEY(estado_civil_id) REFERENCES estados_civiles(id),
    CONSTRAINT fk_nacionalidad_reporte
        FOREIGN KEY(nacionalidad_id) REFERENCES nacionalidades(id),
    CONSTRAINT fk_nivel_estudio_reporte
        FOREIGN KEY(nivel_estudio_id) REFERENCES niveles_estudio(id),
    CONSTRAINT fk_ocupacion_reporte
        FOREIGN KEY(ocupacion_id) REFERENCES ocupaciones(id),
    CONSTRAINT fk_tipo_ingreso_reporte
        FOREIGN KEY(ingreso_id) REFERENCES tipos_ingreso(id),
    CONSTRAINT fk_tipo_seguridad_social_reporte
        FOREIGN KEY(tipo_seguridad_social_id) REFERENCES tipos_seguridad_social(id),
    CONSTRAINT fk_identidad_reporte
        FOREIGN KEY(identidad_id) REFERENCES identidades(id)
);