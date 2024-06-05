# Creamos la tabla de las especialidades 

CREATE TABLE `empresas`.`especialidad` (
  `idespecialidad` INT NOT NULL,
  `nombreespecialidad` VARCHAR(90) NOT NULL,
  `especial` INT NULL,
  `codigo` VARCHAR(10) NULL,
  PRIMARY KEY (`idespecialidad`));



# Editamos la tabla para meter la columna de codespecialidad

ALTER TABLE `empresas`.`especialidad` 
ADD COLUMN `codespecialidad` VARCHAR(10) NULL AFTER `codigo`;

# Ejecutamos el codigo 01_separar_codigo_especialidades

# Metemos las especialidades de vespertino
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('49', 'DESARROLLO DE APLICACIONES MULTIPLATAFORMA VESPERTINO', '2GSHV', 'IFC302V');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('50', 'AUTOMATIZACIÓN Y ROBÓTICA INDUSTRIAL ', '2GSFV', 'ELE303V');

# Metemos las especialidades de dual
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('51', 'DESARROLLO DE APLICACIONES MULTIPLATAFORMA VESPERTINO DUAL', '2GSHV', 'IFC302VD');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('52', 'AUTOMATIZACIÓN Y ROBÓTICA INDUSTRIAL VESPERTINO DUAL', '2GSFV', 'ELE303VD');
UPDATE `empresas`.`especialidad` SET `nombreespecialidad` = 'AUTOMATIZACIÓN Y ROBÓTICA INDUSTRIAL VESPERTINO' WHERE (`idespecialidad` = '50');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('53', 'DESARROLLO DE APLICACIONES MULTIPLATAFORMA DUAL', '2GSH', 'IFC302D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('54', 'AUTOMATIZACIÓN Y ROBÓTICA INDUSTRIAL DUAL', '2GSF', 'ELE303D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('55', 'INSTALACIONES DE TELECOMUNICACIONES DUAL', '2GMC', 'ELE203D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('56', 'AUTOMOCIÓN DUAL', '2GSJ', 'TMV301D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('57', 'ELECTROMECÁNICA DE VEHÍCULOS AUTOMÓVILES DUAL', '2GM', 'TMV202D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('58', 'INSTALACIONES ELÉCTRICAS Y AUTOMÁTICAS DUAL', '2GMB', 'ELE202D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('59', 'MECANIZADO DUAL', '2GMA', 'FME202D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('60', 'PROGRAMACIÓN DE LA PRODUCCIÓN EN FABRICACIÓN MECÁNICA DUAL', '2GSM', 'FME304D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('61', 'SISTEMAS DE TELECOMUNICACIONES E INFORMÁTICA DUAL', '2GSG', 'ELE304D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('62', 'SISTEMAS ELECTROTÉCNICOS Y AUTOMATIZADOS DUAL', '2GSK', 'ELE302D');
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`, `codigo`, `codespecialidad`) VALUES ('63', 'SISTEMAS MICROINFORMÁTICOS Y REDES DUAL', '2GME', 'IFC201D');

# Metemos una especialidad de FORMACION 
INSERT INTO `empresas`.`especialidad` (`idespecialidad`, `nombreespecialidad`) VALUES ('49', 'ESCUELA - EMPRESA');
UPDATE `empresas`.`especialidad` SET `codespecialidad` = 'FORM' WHERE (`idespecialidad` = '49');


# Metemos los campos para las empresas de empresa-escuela 
ALTER TABLE `empresas`.`ge_empresas` 
ADD COLUMN `interesadobolsa` TINYINT NULL AFTER `observaciones`,
ADD COLUMN `PDB` TINYINT NULL AFTER `interesadobolsa`,
ADD COLUMN `cliente` TINYINT NULL AFTER `PDB`,
ADD COLUMN `proveedor` VARCHAR(45) NULL AFTER `cliente`;

# En contactos metemos el departamento para poder volcar los datos de escuela-empresa 
ALTER TABLE `empresas`.`ge_contactos` 
ADD COLUMN `departamento` VARCHAR(45) NULL AFTER `especialidad`;

# Las empresas mayores de 3000 las marcamos como PDB
UPDATE GE_EMPRESAS 
SET PDB=1 
WHERE IDEMPRESA > 3000

# La especialidad de los contactos se quedaba escasa con 75 y lo pasamos a 100
ALTER TABLE `empresas`.`ge_contactos` 
CHANGE COLUMN `especialidad` `especialidad` VARCHAR(100) CHARACTER SET 'utf8mb4' NOT NULL ;

