-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2019-09-14 15:33:19.276

-- tables
-- Table: Agreem_DinerU
USE dinerUser;
DROP TABLE IF EXISTS Agreem_DinerU;
CREATE TABLE Agreem_DinerU (
    PK_idAgreemXDiner int NOT NULL AUTO_INCREMENT,
    FK_idDiner int NOT NULL,
    FK_idAgreement int NOT NULL,
    CONSTRAINT userXConve_pk PRIMARY KEY (PK_idAgreemXDiner)
);

-- Table: Agreement
DROP TABLE IF EXISTS Agreement;
CREATE TABLE Agreement (
    PK_idAgreement int NOT NULL AUTO_INCREMENT,
    FK_idRestaurant int NOT NULL,
    nameAgreement char(20) NOT NULL,
    desdiscount int NOT NULL,
    cutoffDate date NOT NULL,
    CONSTRAINT convenios_pk PRIMARY KEY (PK_idAgreement)
);

-- Table: DinerUser
DROP TABLE IF EXISTS DinerUser;
CREATE TABLE DinerUser (
    PK_idDiner int NOT NULL,
    FK_idUser int NOT NULL,
    numDocument bigint NOT NULL,
    firstname char(15) NOT NULL,
    secondname char(15) NOT NULL,
    firstLastname char(15) NOT NULL,
    secondLastname char(15) NOT NULL,
    address char(30) NOT NULL,
    telephone bigint NOT NULL,
    payMethod varchar(30) NOT NULL,
    infoProfile varchar(200),
    igUser varchar(40),
    CONSTRAINT UsuarioComensal_pk PRIMARY KEY (PK_idDiner)
);

-- Table: Res_DinerU
DROP TABLE IF EXISTS Res_DinerU;
CREATE TABLE Res_DinerU (
    PK_idResxPers int NOT NULL AUTO_INCREMENT,
    FK_idReservation int NOT NULL,
    FK_idDiner int NOT NULL,
    availableChairs int NOT NULL,
    CONSTRAINT ResxPers_pk PRIMARY KEY (PK_idResxPers)
);

-- Table: Reservation
DROP TABLE IF EXISTS Reservation;
CREATE TABLE Reservation (
    PK_idReservation int NOT NULL AUTO_INCREMENT,
    FK_idRestaurant int NOT NULL COMMENT 'Este atributo es FK de la tabla Restaurante.',
    FK_reservationCreator int NOT NULL,
    FK_idTable int NOT NULL,
    personInCharge varchar(15) NOT NULL,
    reservationDate date NOT NULL,
    reservationHour varchar(15) NOT NULL,
    reservationType varchar(15) NOT NULL,
    cardNumber int NULL,
    reservationTotal int NOT NULL,
    amountOfPeople int NOT NULL,
    reservationStatus varchar(15) NOT NULL,
    comments text NULL,
    CONSTRAINT Reservas_pk PRIMARY KEY (PK_idReservation)
);

-- Table: Restaurant
DROP TABLE IF EXISTS Restaurant;
CREATE TABLE Restaurant (
    PK_idRestaurant int NOT NULL AUTO_INCREMENT,
    name varchar(30) NOT NULL,
    description varchar(100) NOT NULL,
    puntuation int NOT NULL,
    comments text NOT NULL,
    address varchar(15) NOT NULL,
    telephone bigint NOT NULL,
    email varchar(20) NOT NULL,
    CONSTRAINT idRestaurante PRIMARY KEY (PK_idRestaurant)
);

-- Table: User
DROP TABLE IF EXISTS User;
CREATE TABLE User (
    PK_idUser int NOT NULL AUTO_INCREMENT,
    userType int NOT NULL,
    username varchar(20) NOT NULL,
    password varchar(150) NOT NULL,
    email char(50) NOT NULL,
    CONSTRAINT User_pk PRIMARY KEY (PK_idUser)
);

-- Table: VIPMembership
DROP TABLE IF EXISTS VIPMembership;
CREATE TABLE VIPMembership (
    PK_idMembership int NOT NULL AUTO_INCREMENT,
    FK_idDiner int NOT NULL,
    cutDate date NOT NULL,
    CONSTRAINT MembresiaVIP_pk PRIMARY KEY (PK_idMembership)
);

-- foreign keys
-- Reference: Agreem_DinerU_Agreement (table: Agreem_DinerU)
ALTER TABLE Agreem_DinerU ADD CONSTRAINT Agreem_DinerU_Agreement FOREIGN KEY Agreem_DinerU_Agreement (FK_idAgreement)
    REFERENCES Agreement (PK_idAgreement);

-- Reference: Agreement_Restaurant (table: Agreement)
ALTER TABLE Agreement ADD CONSTRAINT Agreement_Restaurant FOREIGN KEY Agreement_Restaurant (FK_idRestaurant)
    REFERENCES Restaurant (PK_idRestaurant);

-- Reference: DinerUser_User (table: DinerUser)
ALTER TABLE DinerUser ADD CONSTRAINT DinerUser_User FOREIGN KEY DinerUser_User (FK_idUser)
    REFERENCES User (PK_idUser);

-- Reference: Membresia_Usuario (table: VIPMembership)
ALTER TABLE VIPMembership ADD CONSTRAINT Membresia_Usuario FOREIGN KEY Membresia_Usuario (FK_idDiner)
    REFERENCES DinerUser (PK_idDiner);

-- Reference: Res_DinerU_DinerUser (table: Res_DinerU)
ALTER TABLE Res_DinerU ADD CONSTRAINT Res_DinerU_DinerUser FOREIGN KEY Res_DinerU_DinerUser (FK_idDiner)
    REFERENCES DinerUser (PK_idDiner);

-- Reference: ResxPers_Reservas (table: Res_DinerU)
ALTER TABLE Res_DinerU ADD CONSTRAINT ResxPers_Reservas FOREIGN KEY ResxPers_Reservas (FK_idReservation)
    REFERENCES Reservation (PK_idReservation);

-- Reference: userXConve_Usuario (table: Agreem_DinerU)
ALTER TABLE Agreem_DinerU ADD CONSTRAINT userXConve_Usuario FOREIGN KEY userXConve_Usuario (FK_idDiner)
    REFERENCES DinerUser (PK_idDiner);

-- Inserciones:
insert into User (PK_idUser, userType, username, password, email) VALUES(1,1,'usuarioPrueba','1234','micorreoprueba@outlook.com');
insert into User (PK_idUser, userType, username, password, email) VALUES(2,1,'Elxavier','yisus','xavi@outlook.com');
insert into User (PK_idUser, userType, username, password, email) VALUES(3,1,'amb18','amb','alejandroMeza@outlook.com');
insert into User (PK_idUser, userType, username, password, email) VALUES(4,1,'willi','front','william@yahoo.es');
insert into User (PK_idUser, userType, username, password, email) VALUES(5,1,'cucho','roman','christiandany@gmail.com');
insert into User (PK_idUser, userType, username, password, email) VALUES(6,1,'SebasT','toro50','storo@hotmail.com');
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into DinerUser (PK_idDiner, FK_idUser,numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod) VALUES(1, 1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito');
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into VIPMembership (FK_idDiner,cutDate) VALUES(1,'15/12/19');
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into Restaurant(name,description,puntuation,comments,address,telephone,email) VALUES('EL cielo', 'Este es un restaurante de lujo ubicado en bogotá',9,'None','cll 105 #45-72',3144789520,'ResElcielo@gmail.com');
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into Agreement(FK_idRestaurant, nameAgreement, desdiscount, cutoffDate) VALUES(1,'convenio El cielo', 10, '24/11/19');
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into Agreem_DinerU(FK_idDiner,FK_idAgreement)VALUES(1,1);
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into Reservation(FK_idRestaurant,FK_reservationCreator,FK_idTable,personInCharge,reservationDate,reservationHour,reservationType,cardNumber,reservationTotal,amountOfPeople,reservationStatus,comments)
    VALUES(1,4,5,'Camilo Rojas','01/10/19','9:00','normal',102394,300000,2,'creada','none');
-----------------------------------------------------------------------------------------------------------------------------------------------
insert into Res_DinerU(FK_idReservation,FK_idDiner,availableChairs)VALUES(1,1,2);   
-- End of file.
