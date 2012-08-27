/*
MyVindula Change - 1.1.40
*/
-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.1.63-0ubuntu0.10.04.1

--
-- Create schema myvindulaDB
--

CREATE DATABASE IF NOT EXISTS myvindulaDB;
USE myvindulaDB;

--
-- Definition of table `myvindulaDB`.`vin_myvindula_confgfuncdetails`
--

DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_confgfuncdetails`;
CREATE TABLE  `myvindulaDB`.`vin_myvindula_confgfuncdetails` (
  `fields` varchar(45) NOT NULL,
  `ativo_edit` tinyint(1) NOT NULL DEFAULT '1',
  `ativo_view` tinyint(1) NOT NULL DEFAULT '1',
  `label` varchar(45) DEFAULT NULL,
  `decription` text,
  `type` varchar(45) NOT NULL,
  `required` tinyint(1) NOT NULL DEFAULT '0',
  `list_values` text,
  `ordem` int(11) NOT NULL,
  `mascara` varchar(45) DEFAULT NULL,
  `area_de_view` varchar(45) NOT NULL,
  PRIMARY KEY (`fields`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `myvindulaDB`.`vin_myvindula_confgfuncdetails`
--

/*!40000 ALTER TABLE `vin_myvindula_confgfuncdetails` DISABLE KEYS */;
LOCK TABLES `vin_myvindula_confgfuncdetails` WRITE;
INSERT INTO `myvindulaDB`.`vin_myvindula_confgfuncdetails` VALUES  ('admission_date',1,1,'Data de Admissão','Digite a data de admissão do funcionário','text',0,'',11,'Data','corporate'),
 ('availability',1,1,'Disponibilidade','Digite a disponibilidade do funcionário','text',0,NULL,26,'','other'),
 ('blogs',1,1,'Blogs','Digite os blogs do funcionário','text',0,'',28,'','other'),
 ('cell_phone',1,1,'Celular','Digite o telefone celular do funcionário','text',0,'',4,'Telefone','contact'),
 ('committess',1,1,'Comissão','Digite a comissão do funcionário','text',0,NULL,20,'','other'),
 ('cost_center',1,1,'Centro de Custo','Digite o centro de custo do funcionário','text',0,'',12,'','corporate'),
 ('cpf',1,1,'CPF','Digite o CPF do funcionário','text',0,NULL,29,'','other'),
 ('customised_message',1,1,'Personalizado 4','Campo para personalizar','text',0,NULL,32,'','other'),
 ('date_birth',1,1,'Data de Nascimento','Digite a data de nascimento do funcionário','text',0,'',7,'Data','personal'),
 ('delegations',1,1,'Personalizado 3','Campo para personalizar','text',0,NULL,31,NULL,'other'),
 ('email',1,1,'E-mail','Digite o e-mail do funcionário','text',0,'',5,'','contact'),
 ('employee_id',1,1,'ID Funcionário','Digite o ID do funcionário','text',0,NULL,6,'','personal'),
 ('enterprise',1,1,'Empresa','Digite o nome da empresa do funcionário','text',0,NULL,9,'','corporate'),
 ('languages',1,1,'Idioma','Digite o idioma do funcionário','list',0,'Inglês - Básico\nInglês - Avançado\nEspanhol - Básico\nEspanhol - Avançado\nAlemão - Básico\nJaponês - Básico\nFrances - Básico\nItaliano - Básico\n',25,'','other'),
 ('location',1,1,'Localização','Digite a localização do funcionário','text',0,NULL,15,'','contact'),
 ('name',1,1,'Nome','Digite o nome do funcionário','text',0,NULL,1,'',''),
 ('nickname',1,1,'Apelido','Digite o apelido do funcionário','text',0,NULL,2,'','personal'),
 ('organisational_unit',1,1,'Unidade organizacional','Digite a unidade organizacional do funcionário','text',0,NULL,13,NULL,'corporate'),
 ('papers_published',1,1,'Artigos Publicados','Digite os artigo publicados do funcionário','text',0,NULL,27,'','other'),
 ('personal_information',1,1,'Informações pessoais','Digite as informações pessoais do funcionário','text',0,NULL,22,'','other'),
 ('phone_number',1,1,'Telefone','Digite o telefone do funcionário','text',0,'',3,'Telefone','contact'),
 ('photograph',1,1,'Foto','Coloque a foto do funcionário','img',0,'',18,'',''),
 ('position',1,1,'Cargo','Digite o cargo do funcionário','text',0,NULL,10,NULL,'corporate'),
 ('postal_address',1,1,'Endereço Postal','Digite o endereço postal do funcionário','text',0,'',16,'Cep','contact'),
 ('profit_centre',1,1,'Centro de Lucro','Digite o centro de lucro do funcionário','text',0,NULL,24,'','corporate'),
 ('projects',1,1,'Projetos','Digite os projetos do funcionário','text',0,NULL,21,'','other'),
 ('pronunciation_name',1,1,'Pronuncia do nome teste','Como se pronuncia o  nome do funcionário','text',0,NULL,19,'','personal'),
 ('registration',1,1,'Matrícula','Digite o número de matrícula do funcionário','text',0,NULL,8,'','corporate'),
 ('reports_to',1,1,'Reporta-se a','Digite a quem o funcionário se reporta','text',0,NULL,14,'','corporate'),
 ('resume',1,1,'Personalizado 2','Campo para personalizar','text',0,NULL,30,'','other'),
 ('skills_expertise',1,1,'Habilidades','Digite as habilidades do funcionário','list',0,'Informática - 10 horas\nSecretariado - 20 Horas\nMarketing - 20 horas\nLogística - 30 Horas\nGestão de empresas - 10 horas\nDesign - 10 horas\nAdministração - 20 Horas\n',23,'','other'),
 ('special_roles',1,1,'Funções Especiais','Digite as funções especiais do funcionário','text',0,NULL,17,'','corporate'),
 ('vin_myvindula_department',1,1,'Departamento',NULL,'text',0,NULL,0,'','');
UNLOCK TABLES;
/*!40000 ALTER TABLE `vin_myvindula_confgfuncdetails` ENABLE KEYS */;


--
-- Definition of table `myvindulaDB`.`vin_myvindula_instance_funcdetails`
--

DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_instance_funcdetails`;
CREATE TABLE  `myvindulaDB`.`vin_myvindula_instance_funcdetails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `date_creation` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;


--
-- Definition of table `myvindulaDB`.`vin_myvindula_dados_funcdetails`
--

DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_dados_funcdetails`;
CREATE TABLE  `myvindulaDB`.`vin_myvindula_dados_funcdetails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_creation` datetime NOT NULL,
  `valor` text,
  `vin_myvindula_confgfuncdetails_fields` varchar(45) NOT NULL,
  `vin_myvindula_instance_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_myvindula_dados_funcdetails_vin_myvindula_instance1` (`vin_myvindula_instance_id`),
  KEY `fk_vin_myvindula_dados_funcdetails_vin_myvindula_confgfuncdet1` (`vin_myvindula_confgfuncdetails_fields`),
  CONSTRAINT `fk_vin_myvindula_dados_funcdetails_vin_myvindula_confgfuncdet1` FOREIGN KEY (`vin_myvindula_confgfuncdetails_fields`) REFERENCES `vin_myvindula_confgfuncdetails` (`fields`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_vin_myvindula_dados_funcdetails_vin_myvindula_instance1` FOREIGN KEY (`vin_myvindula_instance_id`) REFERENCES `vin_myvindula_instance_funcdetails` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=337 DEFAULT CHARSET=latin1;



--
-- Definition of table `myvindulaDB`.`vin_myvindula_photo_user`
--

DROP TABLE IF EXISTS `myvindulaDB`.`vin_myvindula_photo_user`;
CREATE TABLE  `myvindulaDB`.`vin_myvindula_photo_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_creation` datetime NOT NULL,
  `username` varchar(45) NOT NULL,
  `photograph` longblob,
  `thumb` longblob,
  `vin_myvindula_confgfuncdetails_fields` varchar(45) NOT NULL,
  `vin_myvindula_instance_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_vin_myvindula_photo_user_vin_myvindula_confgfuncdetails1` (`vin_myvindula_confgfuncdetails_fields`),
  KEY `fk_vin_myvindula_photo_user_vin_myvindula_instance_funcdetails1` (`vin_myvindula_instance_id`),
  CONSTRAINT `fk_vin_myvindula_photo_user_vin_myvindula_confgfuncdetails1` FOREIGN KEY (`vin_myvindula_confgfuncdetails_fields`) REFERENCES `vin_myvindula_confgfuncdetails` (`fields`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_vin_myvindula_photo_user_vin_myvindula_instance_funcdetails1` FOREIGN KEY (`vin_myvindula_instance_id`) REFERENCES `vin_myvindula_instance_funcdetails` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;



