-- DROP SCHEMA public CASCADE;
-- CREATE SCHEMA public;

-- Eliminación de tablas
DROP TABLE IF EXISTS Seguimiento_Denuncia;
DROP TABLE IF EXISTS Evidencia;
DROP TABLE IF EXISTS Arma;
DROP TABLE IF EXISTS Tipo_Arma;
DROP TABLE IF EXISTS Detalle_Sospechoso;
DROP TABLE IF EXISTS Detalle_Bienes;

DROP TABLE IF EXISTS Bienes;
DROP TABLE IF EXISTS D_Extorsion;
DROP TABLE IF EXISTS D_Violencia_Domestica;
DROP TABLE IF EXISTS D_Delito_Patrimonio;
DROP TABLE IF EXISTS Denuncia;
DROP TABLE IF EXISTS Estado_Denuncia;
DROP TABLE IF EXISTS Tipo_Denuncia;
DROP TABLE IF EXISTS Persona;
DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Comisaria;
DROP TABLE IF EXISTS Distrito;
DROP TABLE IF EXISTS Provincia;
DROP TABLE IF EXISTS Departamento;
DROP TABLE IF EXISTS Tipo_Documento;
DROP TABLE IF EXISTS Rol;
DROP TABLE IF EXISTS Rango;

-- TABLAS PRINCIPALES
CREATE TABLE Rango (
    id_rango SERIAL PRIMARY KEY, 
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE Rol (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE Departamento (
    id_departamento SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE Provincia (
    id_provincia SERIAL PRIMARY KEY,
    id_departamento INT NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento) ON DELETE RESTRICT
);

CREATE TABLE Distrito (
    id_distrito SERIAL PRIMARY KEY,
    id_provincia INT NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    ubigeo CHAR(5) NOT NULL,
    FOREIGN KEY (id_provincia) REFERENCES Provincia(id_provincia) ON DELETE RESTRICT
);

CREATE TABLE Comisaria (
    id_comisaria SERIAL PRIMARY KEY,
    id_distrito INT NOT NULL,
    nombre VARCHAR(30) NOT NULL,
	telefono VARCHAR(30) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_distrito) REFERENCES Distrito(id_distrito) ON DELETE RESTRICT
);

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    dni CHAR(8) NOT NULL,
    nombres VARCHAR(50) NOT NULL,
    ape_paterno VARCHAR(50) NOT NULL,
    ape_materno VARCHAR(50) NOT NULL,
    estado CHAR(1) NOT NULL, -- A:Activo, I:Inactivo, R:Retirado
    codigo_usuario VARCHAR(50) NOT NULL,
    clave VARCHAR(100) NOT NULL,
    id_comisaria INT NOT NULL,
    id_rango INT NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_comisaria) REFERENCES Comisaria(id_comisaria) ON DELETE RESTRICT,
    FOREIGN KEY (id_rango) REFERENCES Rango(id_rango) ON DELETE RESTRICT,
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol) ON DELETE RESTRICT
);

CREATE TABLE Tipo_Documento (
    id_tipo_documento INT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE Persona (
    id_persona SERIAL PRIMARY KEY,
    id_tipo_documento INT NOT NULL,
    documento VARCHAR(20) NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    ape_paterno VARCHAR(50) NOT NULL,
    ape_materno VARCHAR(50) NOT NULL,
    id_distrito INT,
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    estado_civil VARCHAR(30) NOT NULL,
    ocupacion VARCHAR(30) DEFAULT 'Sin ocupación',
    telefono VARCHAR(30),
    correo VARCHAR(50),
    FOREIGN KEY (id_tipo_documento) REFERENCES Tipo_Documento(id_tipo_documento) ON DELETE RESTRICT,
	FOREIGN KEY (id_distrito) REFERENCES Distrito(id_distrito) ON DELETE RESTRICT	
);

CREATE TABLE Tipo_Denuncia (
    id_tipo_denuncia SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE Estado_Denuncia (
    id_estado_denuncia SERIAL PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL
);

CREATE TABLE Denuncia (
    id_denuncia SERIAL PRIMARY KEY,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    hora_registro TIME DEFAULT CURRENT_TIME,
    fecha_incidente DATE NOT NULL,
    hora_incidente TIME,
    lugar_hechos VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    descripcion TEXT NOT NULL,
    id_denunciante INT NOT NULL,
    id_denunciado INT,
    id_tipo_denuncia INT NOT NULL,
    id_estado_denuncia INT NOT NULL,
    FOREIGN KEY (id_denunciante) REFERENCES Persona(id_persona) ON DELETE RESTRICT,
    FOREIGN KEY (id_denunciado) REFERENCES Persona(id_persona) ON DELETE RESTRICT,
    FOREIGN KEY (id_tipo_denuncia) REFERENCES Tipo_Denuncia(id_tipo_denuncia) ON DELETE RESTRICT,
    FOREIGN KEY (id_estado_denuncia) REFERENCES Estado_Denuncia(id_estado_denuncia) ON DELETE RESTRICT
);

-- TIPOS DE DENUNCIA
CREATE TABLE D_Delito_Patrimonio (
    id_denuncia INT PRIMARY KEY,
    tipo_delito VARCHAR(30) NOT NULL,
    monto_estimado NUMERIC(9,2),
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE
);

CREATE TABLE D_Violencia_Domestica (
    id_denuncia INT PRIMARY KEY,
    tipo VARCHAR(30) NOT NULL,
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE
);

CREATE TABLE D_Extorsion (
    id_denuncia INT PRIMARY KEY,
    alias_extorsion VARCHAR(30),
    cantidad INT NOT NULL,
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE
);

-- BIENES
CREATE TABLE Bienes (
    id_bien SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE Detalle_Bienes (
    id_detalle_bien SERIAL PRIMARY KEY,
    id_bien INT NOT NULL,
	marca VARCHAR(30),
	modelo VARCHAR(30),
	unidades INT NOT NULL,
	valor_estimado NUMERIC(9,2),
	descripcion VARCHAR(100),
    id_denuncia INT NOT NULL,
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE,
    FOREIGN KEY (id_bien) REFERENCES Bienes(id_bien) ON DELETE RESTRICT
);

-- SOSPECHOSOS
CREATE TABLE Detalle_Sospechoso (
    id_detalle_sospechoso SERIAL PRIMARY KEY,
    id_denuncia INT NOT NULL,
    dni VARCHAR(20),
    nombres VARCHAR(200),
    descripcion TEXT,
    rol_participacion VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE
);

CREATE TABLE Tipo_Arma (
    id_tipo_arma SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE Arma (
    id_arma SERIAL PRIMARY KEY,
    id_denuncia INT NOT NULL,
    id_tipo_arma INT NOT NULL,
    descripcion VARCHAR(100),       -- descripción física o particular del arma
    cantidad INT DEFAULT 1,         -- cantidad si es aplicable
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo_arma) REFERENCES Tipo_Arma(id_tipo_arma) ON DELETE RESTRICT
);

-- EVIDENCIA
CREATE TABLE Evidencia (
    id_evidencia SERIAL PRIMARY KEY,
    titulo VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200),
    ruta TEXT NOT NULL,
    id_denuncia INT NOT NULL,
    FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE
);

-- SEGUIMIENTO
CREATE TABLE Seguimiento_Denuncia (
    id_seguimiento SERIAL PRIMARY KEY,
	id_usuario INT NOT NULL,
    id_denuncia INT NOT NULL,
    fecha DATE NOT NULL,
    accion VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
	FOREIGN KEY (id_denuncia) REFERENCES Denuncia(id_denuncia) ON DELETE CASCADE
);
