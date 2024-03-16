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

# Metemos las especialidades de dual y vespertino

