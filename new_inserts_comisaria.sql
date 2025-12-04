---------------------------------------------------------
-- Eliminar datos en orden inverso a las dependencias  --
---------------------------------------------------------

DELETE FROM Seguimiento_Denuncia;
DELETE FROM Evidencia;
DELETE FROM Arma;
DELETE FROM Tipo_Arma;
DELETE FROM Detalle_Sospechoso;
DELETE FROM Detalle_Bienes;

DELETE FROM Bienes;
DELETE FROM D_Extorsion;
DELETE FROM D_Violencia_Domestica;
DELETE FROM D_Delito_Patrimonio;
DELETE FROM Denuncia;

DELETE FROM Estado_Denuncia;
DELETE FROM Tipo_Denuncia;
DELETE FROM Persona;
DELETE FROM Usuario;
DELETE FROM Comisaria;
DELETE FROM Distrito;
DELETE FROM Provincia;
DELETE FROM Departamento;
DELETE FROM Tipo_Documento;
DELETE FROM Rol;
DELETE FROM Rango;

-- select * from usuario


----------------------------
--   CREACIÓN DE INSERTS  --
----------------------------

------------------------------------
-- RANGO
INSERT INTO Rango (id_rango,nombre) VALUES
(1,'Suboficial de tercera'),
(2,'Suboficial de segunda'),
(3,'Suboficial de primera'),
(4,'Suboficial Brigadier'),
(5,'Suboficial Superior'),
(6,'Alférez'),
(7,'Teniente'),
(8,'Capitán'),
(9,'Mayor');

SELECT setval('rango_id_rango_seq', 9, true);

------------------------------------
-- ROL
INSERT INTO Rol (id_rol, nombre) VALUES
(1, 'Administrador'),
(2, 'Patrulla'),
(3, 'Investigador'),
(4, 'Jefe de unidad');

SELECT setval('rol_id_rol_seq', 4, true);

------------------------------------
-- DEPARTAMENTO
INSERT INTO Departamento (id_departamento, nombre) VALUES
(1, 'Lima'),
(2, 'Cusco'),
(3, 'Arequipa'),
(4, 'Piura'),
(5, 'La Libertad'),
(6, 'Loreto'),
(7, 'Junín'),
(8, 'Lambayeque');

SELECT setval('departamento_id_departamento_seq', 8, true);

------------------------------------
-- PROVINCIA
INSERT INTO Provincia (id_provincia, id_departamento, nombre) VALUES
-- Lima
(1, 1, 'Lima'),
(2, 1, 'Huaral'),
(3, 1, 'Cañete'),
(4, 1, 'Barranca'),
(5, 1, 'Huarochirí'),
-- Cusco
(6, 2, 'Cusco'),
(7, 2, 'Urubamba'),
(8, 2, 'La Convención'),
-- Arequipa
(9, 3, 'Arequipa'),
(10, 3, 'Camana'),
(11, 3, 'Caravelí'),
-- Piura
(12, 4, 'Piura'),
(13, 4, 'Sullana'),
(14, 4, 'Sechura'),
-- La Libertad
(15, 5, 'Trujillo'),
(16, 5, 'Chepén'),
(17, 5, 'Pacasmayo'),
-- Loreto
(18, 6, 'Iquitos'),
(19, 6, 'Maynas'),
-- Junín
(20, 7, 'Huancayo'),
(21, 7, 'Chanchamayo'),
-- Lambayeque
(22, 8, 'Chiclayo'),
(23, 8, 'Lambayeque'),
(24, 8, 'Ferreñafe');

SELECT setval('provincia_id_provincia_seq', 24, true);

------------------------------------
-- DISTRITO
INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Lima (id_provincia 1)
(1, 1, 'Lima', '15001'),
(2, 1, 'Miraflores', '15002'),
(3, 1, 'San Isidro', '15003'),
-- Provincia: Huaral (id_provincia 2)
(4, 2, 'Huaral', '15011'),
(5, 2, 'Aucallama', '15012'),
(6, 2, 'Chancay', '15013'),
-- Provincia: Cañete (id_provincia 3)
(7, 3, 'San Vicente', '15021'),
(8, 3, 'Imperial', '15022'),
(9, 3, 'Asia', '15023'),
-- Provincia: Barranca (id_provincia 4)
(10, 4, 'Barranca', '15031'),
(11, 4, 'Paramonga', '15032'),
(12, 4, 'Pativilca', '15033'),
-- Provincia: Huarochirí (id_provincia 5)
(13, 5, 'Matucana', '15041'),
(14, 5, 'Antioquía', '15042'),
(15, 5, 'San Mateo', '15043');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Cusco (id_provincia 6)
(16, 6, 'Cusco', '08001'),
(17, 6, 'San Sebastián', '08002'),
(18, 6, 'Wanchaq', '08003'),
-- Provincia: Urubamba (id_provincia 7)
(19, 7, 'Urubamba', '08011'),
(20, 7, 'Ollantaytambo', '08012'),
(21, 7, 'Machu Picchu', '08013'),
-- Provincia: La Convención (id_provincia 8)
(22, 8, 'Quillabamba', '08021'),
(23, 8, 'Echarate', '08022'),
(24, 8, 'Santa Ana', '08023');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Arequipa (id_provincia 9)
(25, 9, 'Cayma', '04001'),
(26, 9, 'Cerro Colorado', '04002'),
(27, 9, 'Yanahuara', '04003'),
-- Provincia: Camana (id_provincia 10)
(28, 10, 'Camaná', '04011'),
(29, 10, 'José María Quimper', '04012'),
(30, 10, 'Ocoña', '04013'),
-- Provincia: Caravelí (id_provincia 11)
(31, 11, 'Caravelí', '04021'),
(32, 11, 'Atico', '04022'),
(33, 11, 'Yauca', '04023');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Piura (id_provincia 12)
(34, 12, 'Piura', '20001'),
(35, 12, 'Veintiséis de Octubre', '20002'),
(36, 12, 'Castilla', '20003'),
-- Provincia: Sullana (id_provincia 13)
(37, 13, 'Sullana', '20011'),
(38, 13, 'Bellavista', '20012'),
(39, 13, 'Marcavelica', '20013'),
-- Provincia: Sechura (id_provincia 14)
(40, 14, 'Sechura', '20021'),
(41, 14, 'Rinconada Llicuar', '20022'),
(42, 14, 'Vice', '20023');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Trujillo (id_provincia 15)
(43, 15, 'Trujillo', '13001'),
(44, 15, 'El Porvenir', '13002'),
(45, 15, 'Florencia de Mora', '13003'),
-- Provincia: Chepén (id_provincia 16)
(46, 16, 'Chepén', '13011'),
(47, 16, 'Pacanga', '13012'),
(48, 16, 'Pueblo Nuevo', '13013'),
-- Provincia: Pacasmayo (id_provincia 17)
(49, 17, 'Pacasmayo', '13021'),
(50, 17, 'San Pedro de Lloc', '13022'),
(51, 17, 'San José', '13023');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Iquitos (id_provincia 18)
(52, 18, 'Iquitos', '16001'),
(53, 18, 'Belén', '16002'),
(54, 18, 'Punchana', '16003'),
-- Provincia: Maynas (id_provincia 19)
(55, 19, 'Iquitos', '16011'),  -- Repetido como distrito principal de la provincia
(56, 19, 'Nanay', '16012'),
(57, 19, 'Mazán', '16013');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Huancayo (id_provincia 20)
(58, 20, 'Huancayo', '12001'),
(59, 20, 'El Tambo', '12002'),
(60, 20, 'Chilca', '12003'),
-- Provincia: Chanchamayo (id_provincia 21)
(61, 21, 'Chanchamayo', '12011'),
(62, 21, 'San Ramón', '12012'),
(63, 21, 'Vitoc', '12013');

INSERT INTO Distrito (id_distrito, id_provincia, nombre, ubigeo) VALUES
-- Provincia: Chiclayo (id_provincia 22)
(64, 22, 'Chiclayo', '14001'),
(65, 22, 'José Leonardo Ortiz', '14002'),
(66, 22, 'La Victoria', '14003'),
-- Provincia: Lambayeque (id_provincia 23)
(67, 23, 'Lambayeque', '14011'),
(68, 23, 'Túcume', '14012'),
(69, 23, 'Jayanca', '14013'),
-- Provincia: Ferreñafe (id_provincia 24)
(70, 24, 'Ferreñafe', '14021'),
(71, 24, 'Cañaris', '14022'),
(72, 24, 'Incahuasi', '14023');

-- SELECT setval('distrito_id_distrito_seq', 72, true);

------------------------------------
-- COMISARIA
INSERT INTO Comisaria (id_comisaria, nombre, telefono, direccion, id_distrito) VALUES
(1,'Comisaría Central', '970000001', 'Av. Principal 100', 1),
(2,'Comisaría Sur', '970000002', 'Calle Secundaria 200', 2);

SELECT setval('comisaria_id_comisaria_seq', 2, true);

------------------------------------
-- USUARIO
INSERT INTO Usuario (dni, nombres, ape_paterno, ape_materno, estado, codigo_usuario, clave, id_comisaria, id_rango, id_rol) VALUES
-- Comisaría 1
('70000001', 'Luis Alberto', 'Gómez', 'Huamán', 'A', 'LA-GO-ADM-001', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 1, 8, 1), -- Capitán Admin
('70000002', 'Juan Pablo', 'Quispe', 'Lozano', 'A', 'JP-QU-INV-001', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 1, 1, 3), -- Suboficial Investigador
('70000003', 'Mario', 'Chávez', 'Núñez', 'A', 'MA-CH-INV-002', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 1, 1, 3), -- Suboficial Investigador
('70000004', 'Pedro', 'Salazar', 'Mendoza', 'A', 'PE-SA-PATR-001', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 1, 1, 2), -- Suboficial Patrulla
-- Comisaría 2
('70000005', 'Carlos Enrique', 'Ramos', 'Vargas', 'A', 'CE-RA-ADM-002', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 2, 8, 1), -- Suboficial Superior Admin
('70000006', 'Fernando', 'Torres', 'Cano', 'A', 'FE-TO-INV-003', '$2b$12$GN6y6cs58eCMdRDY0eDYC.s4HiT6Z58pXdjLy9epolqcucojdTqGq', 2, 1, 3); -- Suboficial Investigador

-- SELECT setval('usuario_id_usuario_seq', 6, true);

------------------------------------
-- TIPO DOCUMENTO
INSERT INTO Tipo_Documento (id_tipo_documento, nombre) VALUES
(1, 'DNI'),
(2, 'Pasaporte'),
(3, 'Carnet de extranjería');

-- SELECT setval('tipo_documento_id_tipo_documento_seq', 3, true); -- aún vacío

------------------------------------
-- PERSONA
INSERT INTO Persona (id_persona, id_tipo_documento, documento, nombre, ape_paterno, ape_materno, id_distrito, fecha_nacimiento, direccion, estado_civil, ocupacion, telefono, correo) VALUES
(1, 1, '40123456', 'Ana Sofía', 'Ramírez', 'Díaz', 1, '1985-05-15', 'Av. La Molina 123', 'Casado(a)', 'Arquitecta', '987654321', 'ana.ramirez@mail.com'),
(2, 1, '41987654', 'Beatriz Elena', 'Soto', 'Vega', 2, '1992-11-20', 'Calle Los Sauces 456', 'Soltero(a)', 'Ama de Casa', '998877665', 'beatriz.soto@mail.com'),
(3, 1, '42345678', 'Carlos Daniel', 'Flores', 'Pérez', 3, '1978-01-30', 'Jirón Puno 789', 'Divorciado(a)', 'Empresario', '900112233', 'carlos.flores@mail.com'),
(4, 1, '43765432', 'David Alonso', 'Rojas', 'Manco', 2, '1988-08-25', 'Calle Los Sauces 456', 'Casado(a)', 'Vendedor', NULL, NULL),
(5, 2, 'A1234567', 'Desconocido', 'NN', 'NN', 1, '1900-01-01', 'Sin dirección conocida', 'Soltero(a)', 'Sin ocupación', NULL, NULL);

-- SELECT setval('persona_id_persona_seq', 5, true); -- Actualizamos la secuencia para el siguiente INSERT

------------------------------------
-- TIPO DENUNCIA
INSERT INTO Tipo_Denuncia (id_tipo_denuncia, nombre) VALUES
(1, 'Delito patrimonial'),
(2, 'Violencia doméstica'),
(3, 'Extorsión');

SELECT setval('tipo_denuncia_id_tipo_denuncia_seq', 3, true);

------------------------------------
-- ESTADO DENUNCIA
INSERT INTO Estado_Denuncia (id_estado_denuncia, nombre) VALUES
(1, 'Registrada'),
(2, 'En investigación'),
(3, 'Cerrada'),
(4, 'Archivada');

SELECT setval('estado_denuncia_id_estado_denuncia_seq', 4, true);

------------------------------------
-- DENUNCIA

-- SELECT setval('denuncia_id_denuncia_seq', 1, true);

------------------------------------
-- D_DELITO_PATRIMONIO

------------------------------------
-- D_EXTORSION

------------------------------------
-- D_VIOLENCIA_FAMILIAR

------------------------------------
INSERT INTO Bienes (id_bien, nombre) VALUES
(1, 'Movil'),
(2, 'Computadora portátil'),
(3, 'Dinero Efectivo'),
(4, 'Motocicleta'),
(5, 'Automovil'),
(6, 'Dispositivos domésticos'),
(7, 'Electrodomésticos'),
(8, 'Joyería'),
(9, 'Prendas'),
(10, 'Inmueble');

SELECT setval('bienes_id_bien_seq', 10, true);

------------------------------------
-- DETALLE BIENES

-- SELECT setval('detalle_bienes_id_detalle_bien_seq', 1, true);

------------------------------------
-- TIPO ARMA
INSERT INTO Tipo_Arma (id_tipo_arma, nombre) VALUES
(1, 'Arma de fuego'),
(2, 'Arma blanca'),
(3, 'Contundente'),
(4, 'Explosivo');

-- SELECT setval('tipo_arma_id_tipo_arma_seq', 4, true);

------------------------------------
-- ARMA

-- SELECT setval('arma_id_arma_seq', 1, true);

------------------------------------
-- DETALLE SOSPECHOSO

-- SELECT setval('detalle_sospechoso_id_detalle_sospechoso_seq', 1, true);

------------------------------------
-- EVIDENCIA

-- SELECT setval('evidencia_id_evidencia_seq', 1, true);

------------------------------------
-- SEGUIMIENTO DENUNCIA

-- SELECT setval('seguimiento_denuncia_id_seguimiento_seq', 1, true);

