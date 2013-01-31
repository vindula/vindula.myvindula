SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `myvindulaDB` DEFAULT CHARACTER SET latin1 ;
USE `myvindulaDB` ;

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_comments` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_comments` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(45) NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `type` VARCHAR(45) NULL DEFAULT NULL ,
  `id_obj` VARCHAR(45) NULL DEFAULT NULL ,
  `isPlone` TINYINT(1) NOT NULL DEFAULT '0' ,
  `text` TEXT NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 25
DEFAULT CHARACTER SET = latin1;




-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_confgfuncdetails`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_confgfuncdetails` ;

CREATE TABLE  `myvindulaDB`.`vin_myvindula_confgfuncdetails` (
  `fields` varchar(45) NOT NULL,
  `ativo_edit` tinyint(1) DEFAULT '1',
  `ativo_view` tinyint(1) DEFAULT '1',
  `label` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`fields`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_courses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_courses` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_courses` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `title` VARCHAR(45) NOT NULL ,
  `length` VARCHAR(45) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_department`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_department` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_department` (
  `uid_plone` VARCHAR(45) NOT NULL ,
  `vin_myvindula_funcdetails_id` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`uid_plone`, `vin_myvindula_funcdetails_id`) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_funcdetail_couses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_funcdetail_couses` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_funcdetail_couses` (
  `vin_myvindula_courses_id` INT(11) NOT NULL ,
  `vin_myvindula_funcdetail_username` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`vin_myvindula_courses_id`, `vin_myvindula_funcdetail_username`) ,
  INDEX `fk_vin_myvindula_funcdetail_couses_vin_myvindula_courses1` (`vin_myvindula_courses_id` ASC) ,
  CONSTRAINT `fk_vin_myvindula_funcdetail_couses_vin_myvindula_courses1`
    FOREIGN KEY (`vin_myvindula_courses_id` )
    REFERENCES `myvindulaDB`.`vin_myvindula_courses` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_languages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_languages` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_languages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `title` VARCHAR(45) NOT NULL ,
  `level` VARCHAR(45) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_funcdetail_languages`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_funcdetail_languages` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_funcdetail_languages` (
  `vin_myvindula_languages_id` INT(11) NOT NULL ,
  `vin_myvindula_funcdetail_username` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`vin_myvindula_languages_id`, `vin_myvindula_funcdetail_username`) ,
  INDEX `fk_vin_myvindula_funcdetail_languages_vin_myvindula_languages1` (`vin_myvindula_languages_id` ASC) ,
  CONSTRAINT `fk_vin_myvindula_funcdetail_languages_vin_myvindula_languages1`
    FOREIGN KEY (`vin_myvindula_languages_id` )
    REFERENCES `myvindulaDB`.`vin_myvindula_languages` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_funcdetails`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_funcdetails` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_funcdetails` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(45) NULL DEFAULT NULL ,
  `phone_number` VARCHAR(45) NULL DEFAULT NULL ,
  `cell_phone` VARCHAR(45) NULL DEFAULT NULL ,
  `email` VARCHAR(45) NULL DEFAULT NULL ,
  `employee_id` VARCHAR(45) NULL DEFAULT NULL ,
  `username` VARCHAR(45) NULL DEFAULT NULL ,
  `date_birth` DATE NULL DEFAULT NULL ,
  `registration` VARCHAR(45) NULL DEFAULT NULL ,
  `position` VARCHAR(45) NULL DEFAULT NULL ,
  `enterprise` VARCHAR(45) NULL DEFAULT NULL ,
  `cost_center` VARCHAR(45) NULL DEFAULT NULL ,
  `admission_date` DATE NULL DEFAULT NULL ,
  `organisational_unit` VARCHAR(45) NULL DEFAULT NULL ,
  `reports_to` VARCHAR(45) NULL DEFAULT NULL ,
  `location` VARCHAR(45) NULL DEFAULT NULL ,
  `postal_address` VARCHAR(45) NULL DEFAULT NULL ,
  `special_roles` VARCHAR(45) NULL DEFAULT NULL ,
--  `photograph` TEXT NULL DEFAULT NULL ,
  `nickname` VARCHAR(45) NULL DEFAULT NULL ,
  `pronunciation_name` VARCHAR(45) NULL DEFAULT NULL ,
  `committess` VARCHAR(45) NULL DEFAULT NULL ,
  `projects` VARCHAR(45) NULL DEFAULT NULL ,
  `personal_information` VARCHAR(45) NULL DEFAULT NULL ,
  `profit_centre` VARCHAR(45) NULL DEFAULT NULL ,
  `availability` VARCHAR(45) NULL DEFAULT NULL ,
  `papers_published` VARCHAR(45) NULL DEFAULT NULL ,
  `teaching_research` VARCHAR(45) NULL DEFAULT NULL ,
  `delegations` VARCHAR(45) NULL DEFAULT NULL ,
  `resume` VARCHAR(45) NULL DEFAULT NULL ,
  `blogs` VARCHAR(45) NULL DEFAULT NULL ,
  `customised_message` TEXT NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_photo_user`
-- -----------------------------------------------------

DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_photo_user` ;

CREATE TABLE  `myvindulaDB`.`vin_myvindula_photo_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `date_creation` datetime NOT NULL,
  `photograph` longblob,
  `thumb` longblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_howareu`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_howareu` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_howareu` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(45) NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `visible_area` VARCHAR(45) NULL DEFAULT NULL ,
  `text` TEXT NULL DEFAULT NULL ,
  `upload_image` LONGBLOB NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 30
DEFAULT CHARACTER SET = latin1;



-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_like`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_like` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_like` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(45) NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `date_transfer` DATETIME NOT NULL ,
  `type` VARCHAR(45) NULL DEFAULT NULL ,
  `id_obj` VARCHAR(45) NULL DEFAULT NULL ,
  `isPlone` TINYINT(1) NOT NULL DEFAULT '0' ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_recados`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_recados` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_recados` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(45) NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `destination` VARCHAR(45) NOT NULL ,
  `text` TEXT NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 30
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_holerite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_holerite` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_holerite` (
  `id` INT(100) NOT NULL AUTO_INCREMENT ,
  `nome` VARCHAR(45) NULL DEFAULT NULL ,
  `cpf` VARCHAR(45) NULL DEFAULT NULL ,
  `matricula` VARCHAR(45) NULL DEFAULT NULL ,
  `cargo` VARCHAR(45) NULL DEFAULT NULL ,
  `cod_cargo` VARCHAR(45) NULL DEFAULT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `competencia` VARCHAR(45) NULL DEFAULT NULL ,
  `empresa` VARCHAR(45) NULL DEFAULT NULL ,
  `cod_empresa` VARCHAR(45) NULL DEFAULT NULL ,
  `endereco_empresa` VARCHAR(70) NULL DEFAULT NULL ,
  `cidade_empresa` VARCHAR(45) NULL DEFAULT NULL ,
  `estado_empresa` VARCHAR(45) NULL DEFAULT NULL ,
  `cnpj_empresa` VARCHAR(45) NULL DEFAULT NULL ,
  `total_vencimento` VARCHAR(45) NULL DEFAULT NULL ,
  `total_desconto` VARCHAR(45) NULL DEFAULT NULL ,
  `valor_liquido` VARCHAR(45) NULL DEFAULT NULL ,
  `salario_base` VARCHAR(45) NULL DEFAULT NULL ,
  `base_Inss` VARCHAR(45) NULL DEFAULT NULL ,
  `base_fgts` VARCHAR(45) NULL DEFAULT NULL ,
  `fgts_mes` VARCHAR(45) NULL DEFAULT NULL ,
  `base_irrf` VARCHAR(45) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_descricao_holerite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_descricao_holerite` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_descricao_holerite` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `codigo` VARCHAR(45) NULL DEFAULT NULL ,
  `descricao` VARCHAR(45) NULL DEFAULT NULL ,
  `ref` VARCHAR(45) NULL DEFAULT NULL ,
  `vencimentos` VARCHAR(45) NULL DEFAULT NULL ,
  `descontos` VARCHAR(45) NULL DEFAULT NULL ,
  `vin_myvindula_holerite_id` INT(100) NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_vin_myvindula_descricao_holerite_vin_myvindula_holerite1` (`vin_myvindula_holerite_id` ASC) ,
  CONSTRAINT `fk_vin_myvindula_descricao_holerite_vin_myvindula_holerite1`
    FOREIGN KEY (`vin_myvindula_holerite_id` )
    REFERENCES `myvindulaDB`.`vin_myvindula_holerite` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_config_documents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_config_documents` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_config_documents` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name_document` VARCHAR(45) NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `flag_ativo` TINYINT(1)  NOT NULL DEFAULT TRUE ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `myvindulaDB`.`vin_myvindula_user_documents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_user_documents` ;

CREATE  TABLE IF NOT EXISTS `myvindulaDB`.`vin_myvindula_user_documents` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `documento` LONGBLOB NOT NULL ,
  `date_creation` DATETIME NOT NULL ,
  `vin_myvindula_funcdetails_username` VARCHAR(45) NOT NULL ,
  `vin_myvindula_config_documents_id` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_vin_myvindula_user_documents_vin_myvindula_config_documents1` (`vin_myvindula_config_documents_id` ASC) ,
  CONSTRAINT `fk_vin_myvindula_user_documents_vin_myvindula_config_documents1`
    FOREIGN KEY (`vin_myvindula_config_documents_id` )
    REFERENCES `myvindulaDB`.`vin_myvindula_config_documents` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 1
DEFAULT CHARACTER SET = latin1;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

