-- Eliminar tablas existentes
DROP TABLE IF EXISTS evidencia CASCADE;
DROP TABLE IF EXISTS detalle_bienes CASCADE;
DROP TABLE IF EXISTS categoria_bienes CASCADE;
DROP TABLE IF EXISTS d_violencia_familiar CASCADE;
DROP TABLE IF EXISTS d_hurto CASCADE;
DROP TABLE IF EXISTS d_asalto CASCADE;
DROP TABLE IF EXISTS denuncia CASCADE;
DROP TABLE IF EXISTS tipo_denuncia CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS comisaria CASCADE;
DROP TABLE IF EXISTS rango CASCADE;
DROP TABLE IF EXISTS rol CASCADE;
DROP TABLE IF EXISTS area CASCADE;
DROP TABLE IF EXISTS persona CASCADE;
DROP TABLE IF EXISTS ubigeo CASCADE;
DROP TABLE IF EXISTS distrito CASCADE;
DROP TABLE IF EXISTS provincia CASCADE;
DROP TABLE IF EXISTS departamento CASCADE;

-- Tablas de ubicación
CREATE TABLE departamento (
    id_departamento serial PRIMARY KEY,
    nombre varchar(100) NOT NULL
);

CREATE TABLE provincia (
    id_provincia serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    id_departamento int NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
);

CREATE TABLE distrito (
    id_distrito serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    id_provincia int NOT NULL,
    FOREIGN KEY (id_provincia) REFERENCES provincia(id_provincia)
);

CREATE TABLE ubigeo (
    id_ubigeo serial PRIMARY KEY,
    codigo char(5) UNIQUE NOT NULL,
    id_distrito int NOT NULL,
    FOREIGN KEY (id_distrito) REFERENCES distrito(id_distrito)
);

-- Tablas principales
CREATE TABLE comisaria (
    id_comisaria serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    direccion varchar(200),
    ubigeo char(5),
    telefono varchar(20),
    FOREIGN KEY (ubigeo) REFERENCES ubigeo(codigo)
);

CREATE TABLE persona (
    id_persona serial PRIMARY KEY,
    dni varchar(15) NOT NULL UNIQUE,
    nombres varchar(100) NOT NULL,
    apellidos varchar(100) NOT NULL,
    fecha_nacimiento date,
    telefono varchar(20),
    direccion varchar(150),
    ubigeo char(5),
    FOREIGN KEY (ubigeo) REFERENCES ubigeo(codigo)
);

CREATE TABLE rango (
    id_rango serial PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    descripcion varchar(150)
);

CREATE TABLE area (
    id_area serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    descripcion varchar(150)
);

CREATE TABLE rol (
    id_rol serial PRIMARY KEY,
    nombre varchar(50) NOT NULL,
    descripcion varchar(150),
    id_area int4,
    FOREIGN KEY (id_area) REFERENCES area(id_area)
);

CREATE TABLE usuario (
    id_usuario serial PRIMARY KEY,
    dni varchar(15) NOT NULL UNIQUE,
    nombres varchar(100) NOT NULL,
    ape_paterno varchar(100) NOT NULL,
    ape_materno varchar(100) NOT NULL,
    codigo_usuario varchar(100),
    estado char(1) DEFAULT 'A',
    id_comisaria int,
    id_rango int,
    id_rol int,
    tipo_usuario char(1),
    FOREIGN KEY (id_comisaria) REFERENCES comisaria(id_comisaria),
    FOREIGN KEY (id_rango) REFERENCES rango(id_rango),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE categoria_bienes (
    id_categoria serial PRIMARY KEY,
    nombre varchar(100) NOT NULL,
    descripcion text
);

CREATE TABLE tipo_denuncia (
    id_tipo serial PRIMARY KEY,
    tipo_denuncia varchar(50) NOT NULL,
    descripcion varchar(150),
    id_area int4,
    FOREIGN KEY (id_area) REFERENCES area(id_area)
);

CREATE TABLE denuncia (
    id_denuncia serial PRIMARY KEY,
    fecha_registro timestamp(6) DEFAULT CURRENT_TIMESTAMP,
    fecha_acto date,
    lugar_hechos varchar(200) NOT NULL,
    descripcion text NOT NULL,
    estado char(1) DEFAULT 'P',
    id_denunciante int4 NOT NULL,
    id_denunciado int4,
    id_usuario int4 NOT NULL,
    id_tipo_denuncia int4 NOT NULL,
    ubigeo char(5),
    FOREIGN KEY (id_denunciante) REFERENCES persona(id_persona),
    FOREIGN KEY (id_denunciado) REFERENCES persona(id_persona),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_tipo_denuncia) REFERENCES tipo_denuncia(id_tipo),
    FOREIGN KEY (ubigeo) REFERENCES ubigeo(codigo)
);

CREATE TABLE d_asalto (
    id_denuncia int PRIMARY KEY,
    hubo_violencia bool,
    FOREIGN KEY (id_denuncia) REFERENCES denuncia(id_denuncia)
);

CREATE TABLE d_hurto (
    id_denuncia int PRIMARY KEY,
    circunstancias varchar(200),
    FOREIGN KEY (id_denuncia) REFERENCES denuncia(id_denuncia)
);

CREATE TABLE detalle_bienes (
    id_detalle serial PRIMARY KEY,
    id_denuncia int NOT NULL,
    id_categoria int NOT NULL,
    nombre varchar(200) NOT NULL,
    monto_asciende numeric(12,2),
    descripcion text,
    tipo_bien varchar(50),
    FOREIGN KEY (id_denuncia) REFERENCES denuncia(id_denuncia),
    FOREIGN KEY (id_categoria) REFERENCES categoria_bienes(id_categoria)
);

CREATE TABLE d_violencia_familiar (
    id_denuncia int PRIMARY KEY,
    tipo_violencia varchar(50),
    relacion_agresor varchar(50),
    medidas_proteccion bool,
    FOREIGN KEY (id_denuncia) REFERENCES denuncia(id_denuncia)
);

CREATE TABLE evidencia (
    id_evidencia serial PRIMARY KEY,
    id_denuncia int NOT NULL,
    tipo varchar(50),
    url_archivo varchar(200),
    descripcion text,
    FOREIGN KEY (id_denuncia) REFERENCES denuncia(id_denuncia)
);
