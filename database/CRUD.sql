/* CRUD MYSQL CHIMUEFOX
   AUTOR: ALEJANDRO MEZA
   ULT FECHA MOD: 13/10/2019
   FUNCIONES Y PROCEDIMIENTO ALMACENADOS.
*/           

/* Insercion, modificacion y eliminacion de registros de ejemplo:  */


--Inserciones:
insert into User (userType, username, password, email) VALUES(1,'usuarioPrueba','1234','micorreoprueba@outlook.com');
insert into User (userType, username, password, email) VALUES(1,'Elxavier','yisus','xavi@outlook.com');
insert into User (userType, username, password, email) VALUES(1,'amb18','amb','alejandroMeza@outlook.com');
insert into User (userType, username, password, email) VALUES(1,'willi','front','william@yahoo.es');
insert into User (userType, username, password, email) VALUES(1,'cucho','roman','christiandany@gmail.com');
insert into User (userType, username, password, email) VALUES(1,'SebasT','toro50','storo@hotmail.com');
insert into DinerUser (FK_idUser,numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod) VALUES(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito');
--Deletes:
delete from User where userType = 2;
delete from User where username = 'elTito';
--Updates:  
update DinerUser set telephone=3154879520 where PK_idDiner = 1;
update User set PK_idUser = 7 where username = 'elTito';
update DinerUser set igUser = 'CBerrioL' where PK_idDiner = 2;
--Comando utiles:
SET GLOBAL log_bin_trust_function_creators = 1; --activar la creación de funciones en mysql
SET SQL_SAFE_UPDATES = 0; --desactivar modo safe que impide eliminar y modificar registros
DROP DATABASE chimuefox;
create database chimuefox;
use chimuefox;
--ALTERS
alter table DinerUser modify numDocument bigint not null;
alter table DinerUser modify telephone bigint not null;
alter table Restaurant modify description varchar(100) not null;
alter table Restaurant modify telephone bigint not null;
alter table DinerUser add infoProfile varchar(200);
-----------------------------------------------------------------------------------------------------------------------------------------------
--ejemplo de funcion en mysql
delimiter $$
CREATE function sumar(n1 int, n2 int)
RETURNS INT
BEGIN
  declare suma int;
  set suma = n1 + n2;
  return suma;
END$$

delimiter ;

select sumar(5,5);
--------------------------------------------------------------------------------------
/* CREACION DE FUNCIONES */
drop function validarCedula;

/*Funcion que retorna booleano, si la cedula se encuentra registrada o no en la tabla de DinerUser*/
delimiter $$ --necesario por sintaxis MYSQL
CREATE function validarCedula(cedula int)
RETURNS BOOLEAN
BEGIN
  declare consulta int;
  select PK_idDiner into consulta from DinerUser where numDocument = cedula;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;

select validarCedula(1045454);
--------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si el username se encuentra registrado o no en la tabla User*/
delimiter $$
CREATE function validarNickname(user varchar(20))
RETURNS BOOLEAN
BEGIN
  declare consulta int;
  select PK_idUser into consulta from User where username = user;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;
select validarNickname('amb18');
--------------------------------------------------------------------------------------
delimiter $$
CREATE function getUserIdByNick(user varchar(20))
RETURNS INT
BEGIN
  declare consulta int;
  select PK_idUser into consulta from User where username = user;
  RETURN consulta;
END$$
delimiter ;

--------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si el id de usuario se encuentra registrado o no en la tabla User*/

delimiter $$
CREATE function validarUsuario(iduser int)
RETURNS BOOLEAN
BEGIN
  declare consulta varchar(20);
  select username into consulta from User where PK_idUser = iduser;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;

select validarUsuario(1);

--------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si el id de comensal se encuentra registrado o no en la tabla DinerUser*/

delimiter $$
CREATE function validarComensal(idDiner int)
RETURNS BOOLEAN
BEGIN
declare consulta bigint;
  select numDocument into consulta from DinerUser where PK_idDiner = idDiner;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;

select validarComensal(1);

--------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si la fecha es valida(es mayor a la fecha actual) o no en la tabla de membresias*/

delimiter $$
CREATE function validarFechaCorte(fecha date)
RETURNS BOOLEAN
BEGIN
declare consulta date;
  set consulta = CURDATE();
  
  if consulta > fecha then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;

select validarFechaCorte('2019-09-13'); --FORMATO FECHA: yyyy-mm-dd

--------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si el id de convenio se encuentra registrado  o no en la tabla de convenios*/

delimiter $$
CREATE function validarConvenio(idConvenio int)
RETURNS BOOLEAN
BEGIN
declare consulta char(20);
  select nameAgreement into consulta from Agreement where PK_idAgreement = idConvenio;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;

select validarConvenio(2);

--------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si el DinerUser tiene membresia o no*/

delimiter $$
CREATE function userVIP(idDinerUser int)
RETURNS BOOLEAN
BEGIN
declare consulta int;
  select PK_idMembership into consulta from VIPMembership where FK_idDiner = idDinerUser;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Funcion que retorna los nombres y apellidos de un usuario segun el idDiner pasado por parametro*/
delimiter $$
CREATE function getNamesAndLastnames(idUser int)
RETURNS VARCHAR(50)
BEGIN
  declare consulta varchar(50);
  
  select concat_ws(' ', firstname, secondname, firstLastname, secondLastname) into consulta from DinerUser where PK_idDiner = idUser;
  RETURN consulta;
  
END$$
delimiter ;

select getNamesAndLastnames(1);
/*
select concat_ws(' ', firstname, secondname, firstLastname, secondLastname) into firstN, secondN, firstL, secondL from DinerUser where PK_idUser = idUser;
SELECT concat_ws(' ', nombre, apellidos) as persona FROM personas;
*/
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Funcion que retorna el instagram de un usuario segun el idDiner pasado por parametro*/
delimiter $$
CREATE function getIgUser(idUser int)
RETURNS VARCHAR(40)
BEGIN
  declare consulta varchar(40);
  select igUser into consulta from DinerUser where PK_idDiner = idUser;
  RETURN consulta;
END$$
delimiter ;

select getIgUser(2);
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Funcion que retorna booleano, si el correo se encuentra registrado o no en la tabla User*/
delimiter $$
CREATE function verifyEmail(correo char(30))
RETURNS BOOLEAN
BEGIN
  declare consulta char(30);
  select PK_idUser into consulta from User where email = correo ;
  if consulta is null then
    RETURN False;
  else
    RETURN True;
  end if;
END$$
delimiter ;
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Funcion que verifica los datos ingresados para crear una cuenta de usuario, retorna
1 si no hay errores, 2 si el email ya se encuentra registrado ó 3 si el username ya se encuentra registrado */

delimiter $$
CREATE function verifyRegistration(tipo INT, usuario varchar(20) , contrasena varchar(20), correo varchar(30))
RETURNS INT
BEGIN
  declare valueNick int;
  declare valueEmail int;
  set valueNick = validarNickname(usuario);
  set valueEmail = verifyEmail(correo); 
  if valueNick = 0 then
    if valueEmail = 0 then
      call addUser(tipo, usuario, contrasena, correo);
      RETURN 1;
    else 
      RETURN 2; 
    end if;
  else
    RETURN 3;
  end if;
END$$
delimiter ;
--*****************************************************************************************************************************************
--PROCEDIMIENTOS:
/*Procedimiento que crea un usuario en la tabla User*/

delimiter $$
Create procedure addUser(tipo INT,IN usuario varchar(20) ,IN contrasena varchar(20),IN correo varchar(30))
BEGIN
    if validarNickname(usuario) = 0 then
        insert into User (userType, username, password, email) VALUES(tipo,usuario,contrasena,correo);
    else
        select 'Ese nombre de usuario ya existe';
    end if;
END$$

delimiter ;

----------------------------------------------------------------------------------------------------- 512348748
/*Procedimiento que crea un usuario-comensal en la tabla DinerUser*/

delimiter $$
Create procedure add_dinerUser(IN userNick varchar(20), IN cedula INT,IN nombre char(15),IN segundoNombre char(15) ,IN apellido char(15),IN segundoApellido char(15),IN direccion char(30), IN telefono bigint, IN pago varchar(30))
BEGIN
  declare idUsuario int;
  set idUsuario = getUserIdByNick(userNick)
  if validarCedula(cedula) = 0 then
    insert into DinerUser (FK_idUser, numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod) VALUES(idUsuario,cedula , nombre,segundoNombre,apellido,segundoApellido, direccion, telefono, pago);
  else
    select 'Esa identificacion ya esta registrada';
  end if;
END$$
delimiter ;

call add_dinerUser('amb18',1528439127,'carlos','andres','ramos','mendez','cll 5 #54bis-08',3016981201,'tarjeta de credito');
call crearUsuarioComensal(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',3135487452,'tarjeta de credito');
call crearUsuarioComensal(4,1528439127,'carlos','andres','ramos','mendez','cll 5 #54bis-08',3016981201,'tarjeta de credito');

------------------------------------------------------------------------------------------------------------------------------------------------------
/*Procedimiento que crea una membresia en la tabla VIPMembership*/

delimiter $$
create procedure crearMembresia(IN idComensal INT, IN fechaCorte DATE)
BEGIN
  if validarComensal(idComensal) = 1 then
    if validarFechaCorte(fechaCorte) = 1 then
      insert into VIPMembership(FK_idDiner, cutDate) VALUES(idComensal, fechaCorte);
    else
      select 'La fecha de corte ingresada no es valida ';
    end if;
  else
    select 'El id del usuario-comensal no existe';
  end if;
END$$
delimiter ;
call crearMembresia(1, '2020-05-15');

------------------------------------------------------------------------------------------------------------------------------------------------------
/*Procedimiento que crea un registro en la tabla transaccional Agreem_DinerU*/

delimiter $$
create procedure crearAsociacionConvenio(IN idComensal INT, IN idConvenio INT)
BEGIN
  if validarComensal(idComensal) = 1 then
    if validarConvenio(idConvenio) = 1 then
      insert into Agreem_DinerU(FK_idDiner, FK_idAgreement) VALUES(idComensal, idConvenio);
    else
      select 'El id del convenio no existe';
    end if;
  else
    select 'El id del usuario-comensal no existe';
  end if;
END$$
delimiter ;

call crearAsociacionConvenio(1,2);
select * from Agreem_DinerU;
--------------------------------------------------------------------------------------
/*Procedimiento que modifica la fecha de corte de una membresia conociendo el idDiner*/

delimiter $$
create procedure modificarMembresia(IN usuario INT, IN fechaCorte DATE)
BEGIN
  if validarFechaCorte(fechaCorte) = 1 then
      update VIPMembership set cutDate = fechaCorte where FK_idDiner = usuario;
  else
    select 'La fecha de corte ingresada no es valida ';
  end if;
END$$
delimiter ;

call modificarMembresia(1,'2020-02-10');

/*Procedimiento que modifica la fecha de corte de una membresia conociendo la cedula del usuario*/

delimiter $$
create procedure modificarMembresiaCedula(IN cedula BIGINT, IN fechaCorte DATE)
BEGIN
  if validarFechaCorte(fechaCorte) = 1 then
    update VIPMembership inner join DinerUser on (FK_idDiner = PK_idDiner) set cutDate = fechaCorte  where numDocument = cedula;
  else
    select 'La fecha de corte ingresada no es valida ';
  end if;
END$$
delimiter ;

call modificarMembresiaCedula(1453487801,'2019-12-12');

--------------------------------------------------------------------------------------
/*Procedimientos unitarios que modifican los datos de una cuenta de usuario comensal*/

delimiter $$
Create procedure modificarPrimerNombre(IN cedula INT,IN nuevoNombre char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set firstname = nuevoNombre where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

delimiter $$
Create procedure modificarSegundoNombre(IN cedula INT,IN nuevoSegundoNombre char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set secondname = nuevoSegundoNombre where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;
call modificarSegundoNombre(1453487801,'fernando');

delimiter $$
Create procedure modificarApellido(IN cedula INT,IN apellido char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set firstLastname = apellido where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

delimiter $$
Create procedure modificarSegundoApellido(IN cedula INT,IN segundoApellido char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set secondLastname = segundoApellido where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

delimiter $$
Create procedure modificarDireccion(IN cedula INT,IN dir char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set address = dir where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

delimiter $$
Create procedure modificarTelefono(IN cedula INT,IN tel char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set telephone = tel where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

delimiter $$
Create procedure modificarMPago(IN cedula INT,IN metodo char(15))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set payMethod = metodo where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

/*Procedimiento que modifica TODOS los atributos de una cuenta de usuario comensal*/
delimiter $$
Create procedure edit_dinerUser(IN cedula INT,IN nuevoNombre char(15), IN segundoNombre char(15) ,IN apellido char(15),IN segundoApellido char(15),IN direccion char(30), IN telefono bigint,IN pago varchar(30))
BEGIN
    if validarCedula(cedula) = 1 then
        update DinerUser set firstname = nuevoNombre, secondname = segundoNombre, firstLastname = apellido, secondLastname = segundoApellido, address = direccion, telephone = telefono, payMethod = pago where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

call modificarComensal(1453487801,'carlos', 'andres', 'Berrio', 'Lazo', 'cll 22 #13bis-02',3005481201,'bitcoin');
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
--DELETES:
/*Procedimiento que elimina la cuenta de un usuario comensal*/
delimiter $$
Create procedure delete_dinerUser(IN cedula INT)
BEGIN
    if validarCedula(cedula) = 1 then
        delete from DinerUser where numDocument = cedula;
    else
      select 'Esa identificacion no esta registrada';
     end if;
END$$
delimiter ;

call EliminarComensal(1528439127);

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Procedimiento que elimina la membresia actual de un usuario conociendo su id de usuario-comensal*/

delimiter $$
Create procedure EliminarMembresia(IN idDiner INT)
BEGIN
    if validarComensal(idDiner) = 1 then
        delete from VIPMembership where FK_idDiner = idDiner;
    else
      select 'Ese id no esta registrado';
     end if;
END$$
delimiter ;

/*Procedimiento que elimina la membresia actual de un usuario conociendo su cedula*/

delimiter $$
Create procedure EliminarMembresiaCedula(IN cedula BIGINT)
BEGIN
    if validarCedula(cedula) = 1 then
        delete from VIPMembership inner join DinerUser on VIPMembership.FK_idDiner = DinerUser.PK_idDiner where numDocument = cedula;
    else
      select 'Ese id no esta registrado';
     end if;
END$$
delimiter ;

call EliminarMembresiaCedula(1453487801);
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*Procedimiento que consulta los nombres y apellidos de un usuario junto con su intagram sabiendo su idDiner*/
delimiter $$
CREATE procedure getNameIgUserByidUser(IN idUser int)
BEGIN
  declare nombres varchar(50);
  declare inst varchar(40);
  
  set nombres = getNamesAndLastnames(idUser);
  set inst = getIgUser(idUser);
  select nombres, inst;
END$$
delimiter ;
call getNameIgUserByidUser(2);
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
