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


