-- DEPARTAMENTO
INSERT INTO departamento (id_departamento, nombre) VALUES
(1, 'Lima'),
(2, 'Cusco');

-- PROVINCIA
INSERT INTO provincia (id_provincia, nombre, id_departamento) VALUES
(1, 'Lima', 1),
(2, 'Urubamba', 2);

-- DISTRITO
INSERT INTO distrito (id_distrito, nombre, id_provincia) VALUES
(1, 'Miraflores', 1),
(2, 'Ollantaytambo', 2);

-- UBIGEO
INSERT INTO ubigeo (id_ubigeo, codigo, id_distrito) VALUES
(1, '01001', 1),
(2, '01002', 2);

-- COMISARIA
INSERT INTO comisaria (id_comisaria, nombre, direccion, ubigeo, telefono) VALUES
(1, 'Comisaría Central', 'Av. Principal 123', '01001', '0123456789'),
(2, 'Comisaría Norte', 'Av. Norte 456', '01002', '0123456790');

-- AREA
INSERT INTO area (id_area, nombre, descripcion) VALUES
(1, 'Seguridad Ciudadana', 'Área encargada de la seguridad pública'),
(2, 'Investigaciones', 'Área de investigaciones y denuncias');

-- RANGO
INSERT INTO rango (id_rango, nombre, descripcion) VALUES
(1, 'Comisario', 'Máximo rango en la comisaría'),
(2, 'Subcomisario', 'Segundo rango en jerarquía');

-- ROL
INSERT INTO rol (id_rol, nombre, descripcion, id_area) VALUES
(1, 'Administrador', 'Rol con todos los permisos', 1),
(2, 'Investigador', 'Rol encargado de investigaciones', 2);

-- USUARIO
INSERT INTO usuario (id_usuario, dni, nombres, ape_paterno, ape_materno, codigo_usuario, estado, id_comisaria, id_rango, id_rol, tipo_usuario) VALUES
(1, '12345678', 'Juan', 'Perez', 'Lopez', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 'A', 1, 1, 1, 'A'),
(2, '87654321', 'Maria', 'Gomez', 'Diaz', '$2b$12$dZW9gde10Zf/GovDmb1t6O7PO6XrQ1ZJ3xoxFMQbFSbHdfUGhfA0K', 'A', 2, 2, 2, 'B');
-- policia123 y policia456 son los codigos de usaurio

-- TIPO_DENUNCIA
INSERT INTO tipo_denuncia (id_tipo, tipo_denuncia, descripcion, id_area) VALUES
(1, 'Asalto', 'Denuncia por asalto', 1),
(2, 'Hurto', 'Denuncia por hurto', 1),
(3, 'Violencia Familiar', 'Denuncia por violencia familiar', 2);

-- PERSONA
INSERT INTO persona (dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, ubigeo)
VALUES ('12345678', 'Juan Carlos', 'Pérez Gómez', '1990-05-14', '987654321', 'Av. Los Olivos 123', '01001');

INSERT INTO persona (dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, ubigeo)
VALUES ('87654321', 'María Fernanda', 'López Ruiz', '1985-09-22', '912345678', 'Jr. Las Flores 456', '01001');

INSERT INTO persona (dni, nombres, apellidos, fecha_nacimiento, telefono, direccion, ubigeo)
VALUES ('45678912', 'Luis Alberto', 'Torres Mendoza', '1992-03-10', '998877665', 'Calle Central 789', '01002');




