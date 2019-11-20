#IP="127.0.0.1:3000"
IP="159.65.58.193:3000"
"""
historialReservas = [["Cheers Pizza","Calle 10 #36-12","15/12/2020","08:30 p.m.","Manuel Turizo"],
                    ["American Pizza","Carrera 56 #43-09","15/12/2020","08:30 p.m.","Gabriela Ortiz"],
                    ["Mr. Wings","Carrera 12a #26-32","20/12/2020","06:30 p.m.","Fernanda Chupaesta"]]
                    


lista1 = [["Sofia","Gallego","sofia@jave.com","3022118822","sofielfa","carol_alt",
                    "Mr. Wings","misterwings","Carrera 12a #26-32","20/12/2020","06:30 p.m.","www.google.com","Pendiente","1"],
        ["Maria","Zuluaga","maria@jave.com","456789234","marialp","ladani913",
                    "Cheers Pizza","cheerspizza","Calle 10 #36-12","15/12/2020","08:30 p.m.","www.google.com","Pendiente","2"],
        ["Alejandra","Aguirre","aleja@jave.com","45785667","alejaA","nix_luedke",
                    "American Pizza","americanpizzakw","Carrera 56 #43-09","15/12/2020","08:30 p.m.","www.google.com","Pendiente","3"]]

hReservasActuales = [["Cheers Pizza","cheerspizza","Calle 10 #36-12","15/12/2020","08:30 p.m.","www.google.com","4","No","1"],
                    ["American Pizza","americanpizzakw","Carrera 56 #43-09","15/12/2020","08:30 p.m.","www.google.com","2","No","2"],
                    ["Mr. Wings","misterwings","Carrera 12a #26-32","20/12/2020","06:30 p.m.","www.google.com","3","No","3"]]
"""


lista1 = []
lista2 = []

lista3 = []

lista4 = []

lista5 = [] #Tiene los postulantes a mis reservas publicas

hReservasActuales=[]
historialReservas=[]



#request.json['name'] para recibir y usar json de otras paginas
#pip install flask
#pip install flask-mysql
#pip install flask-login
#pip install Flask-WTF
#pip install requests

############################################ name ############################################
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm, EditForm, PasswordForm
from datetime import timedelta
import requests
import hashlib
users=[]

from reservation import reservation
from models import DinerUser, users, getUser

app=Flask(__name__) #web service

############################################ MYSQL CONNECTION ############################################
if IP=="159.65.58.193:3000":
    app.config['MYSQL_HOST']='localhost' #data base ubication -> localhost
    app.config['MYSQL_USER']='admin' #-> admin
    app.config['MYSQL_PASSWORD']='3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2' #->3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2
    app.config['MYSQL_DB']='dinerUser' #data base name -> dinerUser
else:
    app.config['MYSQL_HOST']='localhost' #data base ubication -> localhost
    app.config['MYSQL_USER']='root' #-> admin
    app.config['MYSQL_PASSWORD']='' #->3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2
    app.config['MYSQL_DB']='dinerUser' #data base name -> dinerUser

mySQL=MySQL(app)   #data base connection
##########################################################################################################

################################################ SETTINGS ################################################
app.secret_key=' srguM44wgw45gewregkujfxhgzdgAHqgreggwwerigpewergWwERwrPegQ#$dgvsdgrLla%wg%Q24g5"vEssFDVSEv3Cr3t4SDFewr4tgsfdbvsd'
login_manager=LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

##########################################################################################################


def printArray(a):
    for i in a: print(i)
    print(" ")

##########################################################################################################
##########################################################################################################
##################################APIS TEMPORALES DE OTROS MODULOS########################################
##########################################################################################################
##########################################################################################################
@app.route('/loginLaverde/<string:email>/<string:password>', methods=['GET'])
def loginLaverde(email,password):
    data={"PK_IdUser": 1, "userName": "xg"}
    json=jsonify(Response=2,
                 Content=data)
    return json

@app.route('/registroLaverde/<string:userName>/<string:email>/<string:password>', methods=['GET'])
def registroLaverde(userName, email, password):
    data={"PK_User": 2}
    #data=(userName, email, password)
    json=jsonify(Response=2,
                 Content=data)
    return json


@app.route('/getPostulatedReservationByUserId/<string:userId>', methods=['GET'])
def getPostulatedReservationByUserId(userId):
    data=[
        {"PK_idReservation": 1,
         "FK_idRestaurant": 5,
         "FK_reservationCreator": 2,
         "personInCharge": "Xavier Garzon",
         "reservationDate": "2019-10-28",
         "reservationHour": "19:00"},

        {"PK_idReservation": 2,
         "FK_idRestaurant": 1,
         "FK_reservationCreator": 3,
         "personInCharge": "William Aguirre",
         "reservationDate": "2019-11-18",
         "reservationHour": "20:00"}
        ]
    json=jsonify(Response=2,
                 Content=data)
    return json


@app.route('/getPostulatedByReservationId/<string:reservationId>', methods=['GET'])
def getPostulatedByReservationId(reservationId):
    """
    status=1 accepted
    status=0 stand by
    """
    data=[
        {"PK_idUser": 1,
         "status": 1
        },
        {"PK_idUser": 2,
         "status": 1
        },
        {"PK_idUser": 3,
         "status": 2    
        }
        ]
    json=jsonify(Response=2,
                 Content=data)
    return json

@app.route('/getRestaurantNameById/<string:restaurantId>', methods=['GET'])
def getRestaurantNameById(restaurantId):
    data=""
    if restaurantId=="1"    :
        data="Warner Foods"
    else:
        data="Salchiburguer"
    json=jsonify(Response=2,
                 Content=data)
    return json

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


##########################################################################################################
##########################################################################################################
#########################################APIS DE ESTE MODULOS#############################################
##########################################################################################################
##########################################################################################################

@app.route('/getDinerUserById/<string:id>', methods=['GET'])
def getDinerUserById(id):
    cur=mySQL.connection.cursor()
    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    data=cur.fetchall()
    #data=(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito')
    cur.close()
    try:
        data=data[0]
        json=None
        tmp={"numDocument": data[2],         
            "firstname": data[3],
            "secondname": data[4],
            "firstLastname": data[5],
            "secondLastname": data[6],
            "address": data[7],
            "telephone": data[8],
            "payMethod": data[9],
            "infoProfile": data[10],
            "igUser": data[11]}
        json=jsonify( Response=2,
                      Content=tmp)
    except:
        json=jsonify(Response=1)
    return json


@app.route('/getDinerNameTelByUserId/<string:id>', methods=['GET'])
def getDinerNameTelByUserId(id):
    cur=mySQL.connection.cursor()
    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    data=cur.fetchall()
    #data=(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito')
    cur.close()
    try:
        data=data[0]
        json=None
        tmp={"firstname": data[3],
             "secondname": data[4],
             "firstLastname": data[5],
             "secondLastname": data[6],
             "telephone": data[8]}
        json=jsonify( Response=2,
                      Content=tmp)
    except:
        json=jsonify(Response=1)
    return json


@app.route('/isVIP/<string:id>/', methods=['GET'])
def isVIP(id):
    id=int(id)
    json=None
    try:
        cur=mySQL.connection.cursor()
        cur.callproc('userVIP', [id])
        #cur.close()
        data=cur.fetchall()
        cur.close()
        json=jsonify( Response=2,
                      content=data[0])
    except Exception as e:
        json=jsonify( Response=1)
        print("+++isVIP", e)
    #cursor.stored_results()
    return json
  

@app.route('/createVIPMembership/<string:id>/', methods=['POST'])
def createVIPMembership(idComensal, opc):
    fechaInicio=datetime.date.today()
    idComensal=int(idComensal)
    json=None
    m = 0
    try:
        cur=mySQL.connection.cursor()
        if opc == 1:
            m = datetime.timedelta(months=1)
            fechaCorte = fechaInicio+m
        elif opc == 2:
            m = datetime.timedelta(months=2)
            fechaCorte = fechaInicio+m            
        elif opc == 3:
            m = datetime.timedelta(months=3)
            fechaCorte = fechaInicio+m            
        cur.callproc('createVIPMembership', [idComensal, fechaCorte])
        cur.commit()
        cur.close()
        json=jsonify( Response=2,
                      content=data[0])
    except Exception as e:
        json=jsonify( Response=1)
        print("+++isVIP", e)
    return json


@app.route('/crypto/<string:data>/', methods=['GET'])
def crypto(data):
    #print(data)
    #tmp=getUser("", "", "", "", "",data)
    h = hashlib.sha1()
    h.update(data)
    pas=h    
    pas=str(pas.hexdigest())
    json=None
    #print("pass:", pas)
    try:
        data=pas
        json=jsonify( Response=2,
                      content=data)
    except Exception as e:
        json=jsonify( Response=1)
        #print("+++isVIP", e)
    #cursor.stored_results()
    return json

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
"""
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=5)
"""
def bringUserData():
    ans=1
    try:
        cur=mySQL.connection.cursor()
        cur.execute('SELECT * FROM DinerUser WHERE FK_idUser = {0}'.format(session["PK_IdUser"]))
        data=cur.fetchall()
        #pri(data)                            
        cur.close()
        if len(data)!=0:
            data=data[0]
            #pri("DATA mayor a cero")
            #pri(data)
            if len(data)!=0:
                session["PK_IdUser"]=data[0]
                session["PK_IdDiner"]=data[1]
                session["numDocument"]=data[2]
                session["firstName"]=data[3]
                session["secondName"]=data[4]
                session["firstLastName"]=data[5]
                session["secondLastName"]=data[6]                                
                session["address"]=data[7]
                session["telephone"]=data[8]
                session["infoProfile"]=data[10]    
                session["igUser"]=data[11]
                next_page = request.args.get('next')
    except Exception as e:
        print("+++bringUserData", e)
        flash("bringUserData base de datos Meza", "error")
        ans=0
    return ans
    #return redirect(url_for('login'))

def bringRecordReservation():
    global historialReservas
    url="http://"+"159.65.58.193:8000"+"/api/getReservationsRecordByUserId/"+str(session["PK_IdDiner"])
    #pri("....Record",session["PK_IdDiner"])
    historialReservas=list()
    try:
        response=requests.get(url, params=None, timeout=5)
        if response.status_code==200:
            response=response.json()
            #pri("res", response)
            if response["Response"]==2:
                data=response["Content"]
                #pri("dataaaa", data)
                for restaurant in data:
                    #pri(restaurant)
                    idRestaurant=restaurant["FK_idRestaurant"]
                    url="http://181.50.100.167:5000/getRestaurant/"+str(idRestaurant)
                    tmp=requests.get(url, params=None, timeout=5)
                    if tmp.status_code==200:
                        tmp=tmp.json()
                        if tmp["Response"]==2:
                            tmp=tmp["Content"]
                            individual=list()
                            #pri(tmp)
                            #pri(restaurant)
                            individual.append(str(tmp[0]["name"]))
                            individual.append(str(restaurant["reservationDate"]))
                            individual.append(str(restaurant["reservationHour"]))
                            individual.append(str(tmp[0]["address"]))
                            individual.append(str(restaurant["personInCharge"]))
                            historialReservas.append(individual)
                        else:
                            flash("bringRecordReservation Response API de Cristian:2", "error")
                    else:
                        flash("bringRecordReservation Fallo el API de Cristian", "error")                            
            else:
                flash("bringRecordReservation Response API de LAURA", "error")
        else:
            flash("bringRecordReservation Fallo el API de LAURA", "error")
    except Exception as e:
        print("+++profile ", e)

def bringAllReservation():
    url="http://159.65.58.193:8000/api/getPublicReservationsByUserId/"+str(session["PK_IdDiner"])
    lista1=list()
    usrName=None; usrLastName=None; UsrEmail=None; telephone=None; usrIg=None;
    resName=None; ResIg=None; resAddress=None; date=None; hour=None; status=None;
    availableChairs=None; idReservation=None
    try:
        response=requests.get(url, params=None, timeout=5)
        if response.status_code==200:
            response=response.json()
            if response["Response"]==2:
                data=response["Content"]
                res_final=[len(data)]    #Final reservation with rest name
                for reservation in data:
                    idRestaurant=reservation["FK_idRestaurant"]
                    url="http://181.50.100.167:5000/getRestaurant/"+str(idRestaurant)
                    restaurant=requests.get(url, params=None, timeout=5)
                    if restaurant.status_code==200:
                        restaurant=restaurant.json()
                        if response["Response"]==2:
                            restaurant=restaurant["Content"]
                            restaurant = restaurant[0]
                            cur=mySQL.connection.cursor()
                            #print("#", restaurant)
                            #print("$", reservation)
                            #print("%", reservation["FK_reservationCreator"])
                            cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(str(reservation["FK_reservationCreator"])))
                            data=cur.fetchall()
                            #print("->", data)
                            data=data[0]
                            cur.close()
                            #print(reservation)
                            #print(restaurant)
                            #print("<-", data)
                            pk_id=data[0]
                            usrName=data[3]+" "+data[4]
                            usrLastName=data[5]
                            UsrEmail="prueba@gmail.com"
                            telephone=data[8]
                            usrIg=data[11]                  
                            resName=restaurant["name"]
                            ResIg=restaurant["email"]
                            resAddress=restaurant["address"]
                            date=reservation["reservationDate"]
                            hour=reservation["reservationHour"]
                            status="Pendiente"
                            #availableChairs=reservation["availableChairs"]
                            idReservation=reservation["PK_idReservation"]
                            lista1.append([usrName, usrLastName, UsrEmail, telephone, usrIg ,usrIg, resName, ResIg, resAddress, date, hour, ResIg, status, idReservation, pk_id])
                            #["0 nombre","1 apellido","2 email","3 telefono","4 usuario","5 instagramPerfil",
                            #"6 restaurante","7 instagramRestaurante","8 direccion","9 fecha","10 hora",
                            #"11 URL Restaurante","12 estado (Pendiente siempre)","13 Sillas"]
                            #print(lista1)                        
                        else:
                            flash("bringAllReservation Response 2 el API de CRISTIAN 1", "error")    
                    else:
                        flash("bringAllReservation Fallo el API de CRISTIAN 1", "error")   
            else:
                flash("bringAllReservation Response 2 el API de LAURA 1", "error")    
        else:
            flash("bringAllReservation API de LAURA 1", "error")
    except Exception as e:
        print("bringAllReservation", e)
    #pri("bring lista1 ", lista1)
    """
    reservations=list()
    url="http://"+"159.65.58.193:8000"+"/api/getReservationsRecordByUserId/"+str(session["PK_IdDiner"]) 
    print("bring", url)
    #me trae TODAS las reservas publicas
    try:
        response=requests.get(url, params=None, timeout=5)
        if response.status_code==200:
            response=response.json()
            if response["Response"]==2:
                data=response["Content"]
                for restaurant in data:
                    print("RESTAURANTES")
                    idRestaurant=restaurant["FK_idRestaurant"]
                    url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                    tmp=requests.get(url, params=None, timeout=5)
                    if tmp.status_code==200:
                        tmp=tmp.json()
                        if response["Response"]==2:
                            tmp=tmp["Content"]
                            individual=list()
                            individual.append(str(tmp[0]["name"]))
                            individual.append(str(restaurant["reservationDate"]))
                            individual.append(str(restaurant["reservationHour"]))
                            individual.append(str(tmp[0]["address"]))
                            individual.append(str(restaurant["personInCharge"]))
                            reservations.append(individual)
                        else:
                            flash("Response API de Cristian: 2", "error")
                    else:
                        flash("Fallo el API de Cristian", "error")                            
            else:
                flash("Fallo el API de LAURA", "error")
        else:
            flash("HTTP error", "error")
    except Exception as e:
        print("+++profile ", e)
    return reservations
    """
    return lista1
        
def bringPrivateSelf():
    privateSelf=list() 
    url="http://159.65.58.193:8000/api/getActiveReservationsByUserIdAndType/"+str(session["PK_IdDiner"])+"/0/" #esta url cambia por la de Laura
    # 0 privada, 1 publica
    try:
        response=requests.get(url, params=None, timeout=5)
        if response.status_code==200:
            response=response.json()
            if response["Response"]==2:
                data=response["Content"]
                for restaurant in data:
                    idRestaurant=restaurant["FK_idRestaurant"]
                    url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                    tmp=requests.get(url, params=None, timeout=5)
                    if tmp.status_code==200:
                        tmp=tmp.json()
                        if tmp["Response"]==2:
                            tmp=tmp["Content"]
                            individual=list()
                            individual.append(str(tmp[0]["name"]))
                            individual.append(str(tmp[0]["email"]))
                            individual.append(str(tmp[0]["address"]))
                            individual.append(str(restaurant["reservationDate"]))
                            individual.append(str(restaurant["reservationHour"]))                    
                            individual.append(str(restaurant["availableChairs"]))
                            individual.append("no")
                            individual.append(str(restaurant["PK_idReservation"]))

                            privateSelf.append(individual)
                        else:
                            flash("bringPrivateSelf Response API de Cristian: 2", "error")
                    else:
                        flash("bringPrivateSelf Fallo el API de Cristian", "error")                            
            else:
                flash("bringPrivateSelf Fallo el API de LAURA", "error")
        else:
            flash("bringPrivateSelf API de LAURA error", "error")
    except Exception as e:
        print("+++profile privadas ", e)
    return privateSelf

def bringPublicSelf():
    publicSelf=list()
    url="http://159.65.58.193:8000/api/getActiveReservationsByUserIdAndType/"+str(session["PK_IdDiner"])+"/1/" #esta url cambia por la de Laura
    try:
        response=requests.get(url, params=None, timeout=5)
        if response.status_code==200:
            response=response.json()
            if response["Response"]==2:
                data=response["Content"]
                for restaurant in data:
                    idRestaurant=restaurant["FK_idRestaurant"]
                    url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                    tmp=requests.get(url, params=None, timeout=5)
                    if tmp.status_code==200:
                        tmp=tmp.json()
                        if tmp["Response"]==2:
                            tmp=tmp["Content"]
                            individual=list()
                            individual.append(str(tmp[0]["name"]))
                            individual.append(str(tmp[0]["email"]))
                            individual.append(str(tmp[0]["address"]))
                            individual.append(str(restaurant["reservationDate"]))
                            individual.append(str(restaurant["reservationHour"]))                    
                            individual.append(str(restaurant["availableChairs"]))
                            individual.append("si")
                            individual.append(str(restaurant["PK_idReservation"]))

                            publicSelf.append(individual)
                        else:
                            flash("bringPublicSelf Response API de Cristian: 2", "error")
                    else:
                        flash("bringPublicSelf Fallo el API de Cristian", "error")                            
            else:
                flash("bringPublicSelf Fallo el API de LAURA", "error")
        else:
            flash("bringPublicSelf API de LAURA error", "error")
    except Exception as e:
        print("+++profile publicas ", e)
    return publicSelf


@app.route('/')
def Index():
    #pri(session)
    if "firstName" in session:
        #pri("INDEX")
        #print(session)
        pass
    return render_template('index.html')

    
@app.route('/deleteDinerUserById/<string:id>')
def deleteDinerUserById(id):
    ############################################ DELETE USER TO DB ############################################
    try:
        cur=mySQL.connection.cursor()
        cur.callproc('delete_dinerUser', [id])
        cur.close()
        mySQL.connection.commit()
    except Exception as e:
        print("+++deleteDinerUserById", e)
    ############################################ DELETE USER TO DB ############################################
    #flash('User Deleted Succesfully')
    #pri("DELETED: ",id)
    return redirect(url_for('Index'))   #redirect


#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
@app.route('/login/', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    #pri("LOGIN")
    ok=False
    """
    session["PK_IdUser"]="1"
    session["PK_IdDiner"]="1"
    session["numDocument"]="6543"
    session["firstName"]="William"
    session["secondName"]=""
    session["firstLastName"]="Aguirre"
    session["secondLastName"]=""                                
    session["address"]="Calle 38#35"
    session["telephone"]="456789"
    session["infoProfile"]="Hola"    
    session["igUser"]="williamaguirrezapata"
    """
    
    next_page = request.args.get('next')
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if not ok:
        return redirect(url_for('profile'))
    else:
        #pri("Inicio")
        logged=False
        url="http://181.50.100.167:4000/validateSession?id="+str(session["PK_IdDiner"])
        tmp=requests.get(url, params=None, timeout=5)
        if tmp.status_code==200:
            tmp=tmp.json()
            if tmp["response"]==2:
                logged=True
            else:
                logged=False
        if not logged:
            if form.validate_on_submit():
                ##############################################################################
                email=request.form['email']
                password=request.form['password']
                #pri(password)
                h = hashlib.sha1()
                h.update(password)
                pas=h
                pas=str(pas.hexdigest())
                password=pas
                #user=getUser("", "", "", "", "",password)
                #password=user.password
                #pri(password)
                #url="http://"+IP+"/loginLaverde/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
                #url="http://181.50.100.167:4000/addUser?userName="+str(userName)+"&email="+str(email)+"&password="+password+"&userType=1"
                url="http://181.50.100.167:4000/login?email="+str(email)+"&password="+str(password)
                #5dc9f2fd91aa3d00a3555d69

                #session["PK_IdUser"]=1
                #session["PK_IdDiner"]=1

                #"""
                response=requests.post(url, params=None)
                #pri("Llorelo", response.text)
                
                if response.status_code==200:
                    response=response.json()                
                    #pri("->",response)

                    if response["response"]==2:
                        PK_IdUser=response["content"]["id"]
                        userName=response["content"]["userName"]
                        userType=response["content"]["userType"]
                        #pri("Hola", response["content"])
                        try:
                            
                            #print(len(password), password)
                            #cur=mySQL.connection.cursor()
                            #cur.callproc('login', [email, password])                                        
                            #data=cur.fetchall()
                            #data=data[0][0]
                            #cur.close()
                            #print(data)
                        
                            #pri("VALIDO LOGIN")
                            #ans=bringUserData()
                            
                            #cur=mySQL.connection.cursor()
                            #cur.callproc("getDataDinerUserByEmail", [email])
                            #data=cur.fetchall()                                                        
                            #data=data[0]
                            #cur.close()
                            cur=mySQL.connection.cursor()
                            cur.execute('SELECT * FROM DinerUser WHERE FK_idUser = {0}'.format(PK_IdUser))
                            data=cur.fetchall()
                            #pri(data)                            
                            cur.close()
                            if len(data)!=0:
                                data=data[0]
                                #pri("DATA mayor a cero")
                                #pri(data)
                                if len(data)!=0:
                                    session["PK_IdUser"]=data[0]
                                    session["PK_IdDiner"]=data[1]
                                    session["password"]=password
                                    session["numDocument"]=data[2]
                                    session["firstName"]=data[3]
                                    session["secondName"]=data[4]
                                    session["firstLastName"]=data[5]
                                    session["secondLastName"]=data[6]                                
                                    session["address"]=data[7]
                                    session["telephone"]=data[8]
                                    session["infoProfile"]=data[10]    
                                    session["igUser"]=data[11]
                                    session["email"]=email
                                    next_page = request.args.get('next')
                                    #pri(session)
                            else:
                                flash("Error base de datos Meza", "error")
                                return redirect(url_for('login'))
                            
                            #return redirect(next_page)
                            next_page=None
                            if (not next_page or url_parse(next_page).netloc != ''):
                                flash("Bienvenido "+ session["firstName"], "success")
                                #userType=3
                                if userType==1:
                                    next_page = url_for('profile')
                                elif userType==2:
                                    return redirect('http://181.50.100.167:3000/?id='+str(session["PK_IdUser"]))
                                else:
                                    return redirect('http://181.50.100.167:4001/Principal/?id='+str(session["PK_IdUser"])+'?pass='+str(password)+'?ciudad=1')


                                                        ########### Tinder ##########################################################
                                #bringPublic()
                                return redirect(url_for('login')) 
                        except Exception as e:
                            flash("Datos incorrectos", "error")
                            print("+++login 1", e)    
                else:
                    flash("El usuario o contrasena no estan correctos", "error")
                    print("+++login 2", e)                   
                ##############################################################################
                #"""
        else:
            return redirect(url_for('profile'))


    return render_template('login_form.html', form=form)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    ok=False  
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if not ok and logged:
        return redirect(url_for('profile'))
    else:
        logged=False
        url="http://181.50.100.167:4000/validateSession?id="+str(session["PK_IdDiner"])
        tmp=requests.get(url, params=None, timeout=5)
        if tmp.status_code==200:
            tmp=tmp.json()
            if tmp["response"]==2:
                logged=True
            else:
                logged=False
        if not logged:
            if form.validate_on_submit():
                if request.method == 'POST':
                    numDocument=request.form['numDocument']
                    name=request.form['name']; name=name.split()
                    firstName, secondName = " ", " "
                    if len(name)>1:
                        firstName=str(name[0])
                        secondName=str(name[0]) 
                    else:
                        firstName=str(name[0])

                    lastName=request.form['lastName']; lastName=lastName.split()
                    firstLastName, secondLastName = " ", " "
                    if len(lastName)>1:
                        firstLastName=str(lastName[0])
                        secondLastName=str(lastName[0])
                    else:
                        firstLastName=str(lastName[0])

                    telephone=request.form['telephone']
                    userName=request.form['userName']
                    email=request.form['email']
                    password=request.form['password']
                    password2=request.form['password2']

                    if password==password2:
                        ############################################ ADD USER TO DB ############################################
                        #user=getUser("", "", "", "", "",password)
                        #password=user.password
                        h = hashlib.sha1()
                        h.update(password)
                        pas=h    
                        pas=str(pas.hexdigest())
                        password=pas
                        url="http://181.50.100.167:4000/addUser?userName="+str(userName)+"&email="+str(email)+"&password="+password+"&userType=1"
                        #url="http://"+IP+"/registroLaverde/"+str(userName)+"/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
                        response=requests.post(url, params=None)
                        print(url)
                        print(response.text)
                        if response.status_code==200:
                            response=response.json()
                            if response["response"]==2:
                                address=" "; payMethod=" "
                                #user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password)
                                #password=user.password
                                PK_IdUser=str(response["content"]["id"])
                                print("+++++++++")                
                                #print("->", user.data())
                                print("EEEEEEEEE", password)
                                print(PK_IdUser, address, payMethod)
                                userOk=False; emailOk=False
                                try:                     
                                    print("Maquina")
                                    cur=mySQL.connection.cursor()
                                    cur.callproc('addUser', [PK_IdUser, 1, userName, password, email])                                        
                                    #mySQL.connection.commit()
                                    cur.fetchall()
                                    cur.close()
                                    print("Buenas")

                                    cur=mySQL.connection.cursor()
                                    cur.callproc('add_dinerUser', [PK_IdUser, userName, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, "", userName])                                    
                                    mySQL.connection.commit()
                                    cur.fetchall()
                                    cur.close() 
                                    print("Erda")
                                    
                                    next_page = request.args.get('next', None)
                                    if not next_page or url_parse(next_page).netloc != '':
                                        next_page = url_for('login')
                                    return redirect(next_page)

                                except Exception as e:
                                    print("+++reg", e)
                            else:
                                print("Response", response["response"])
                        else:                        
                            response=response.json()
                            print("error 0", response)
                            print("error 1", response["content"])
                            print()
                            response=response["content"]
                            print("error 3", response["message"])
                            flash(str(response["message"]), "error")
                            #print("error 4", response.status_code)
                    else:
                        flash("La contrasenas no coinciden", "error") 
        else:
            return redirect(url_for('profile'))
    return render_template("signup_form.html", form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    global hReservasActuales, historialReservas, lista1
    ok=False    
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if ok:
        return redirect(url_for('login'))   #redirect
    else:
        logged=False
        url="http://181.50.100.167:4000/validateSession?id="+str(session["PK_IdDiner"])
        tmp=requests.get(url, params=None, timeout=5)
        if tmp.status_code==200:
            tmp=tmp.json()
            if tmp["response"]==2:
                logged=True
            else:
                logged=False
        if logged:
            bringUserData()
            tmp2 = session

            ##########################################################################################################################
            #############################################HISTORIAL DE RESERVAS########################################################
            ##########################################################################################################################
            bringRecordReservation()



            ##########################################################################################################################
            #############################################LISTAR RESERVAS PUBLICAS########################################################
            ##########################################################################################################################
            #bringAllReservation()
            #print("PUBLICAS")
            #for res in lista1:
            #    print(res)


            ##########################################################################################################################
            #############################################  RESERVAS ACTUALES  ########################################################
            ##########################################################################################################################
            hReservasActuales=bringPrivateSelf()
            selfPublic=bringPublicSelf()
            for res in selfPublic:
                hReservasActuales.append(res)
        else:
            return redirect(url_for('login'))   #redirect        

    return render_template("profile_view.html", tmp2=tmp2, historialReservas=historialReservas, hReservasActuales=hReservasActuales)





@app.route('/tinder', methods=['GET', 'POST'])
def tinder():
    global lista1, lista2,  lista5
    ok=False
    #session["PK_IdDiner"]=1
    #lista1=[]
    try:    
        a=(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if ok:
        return redirect(url_for('login'))
    else:
        logged=False
        url="http://181.50.100.167:4000/validateSession?id="+str(session["PK_IdDiner"])
        tmp=requests.get(url, params=None, timeout=5)
        if tmp.status_code==200:
            tmp=tmp.json()
            if tmp["response"]==2:
                logged=True
            else:
                logged=False
        if logged:
            #print(lista1)
            lista1=bringAllReservation()
            lista2=list()
            #print(lista1)
            url="http://159.65.58.193:8000/api/getPostulatedReservationsByUserId/"+str(session["PK_IdDiner"])
            tmp=requests.get(url, params=None, timeout=5)
            if tmp.status_code==200:
                tmp=tmp.json()
                print(200)
                if tmp["Response"]==2:
                    print("Response 2")
                    reservation=tmp["Content"]
                    todos=bringAllReservation()
                    for res in reservation:
                        idReservation=res["PK_idReservation"]
                        idRestaurant=res["FK_idRestaurant"]
                        idCreator=res["FK_reservationCreator"]
                        status=res["status"]
                        date=res["reservationDate"]
                        hour=res["reservationHour"]
                        if status==1:
                            status="Pendiente"
                        elif status==2:
                            stauts="Aceptado"
                        else:
                            status="Rechazado"
                        usrName=None; usrLastName=None; UsrEmail=None; telephone=None; usrIg=None;
                        resName=None; ResIg=None; resAddress=None; status=None;
                        availableChairs=None; idReservation=None
                        try:
                            url="http://181.50.100.167:5000/getRestaurant/"+str(idRestaurant)
                            restaurant=requests.get(url, params=None, timeout=5)
                            if restaurant.status_code==200:
                                restaurant=restaurant.json()
                                if restaurant["Response"]==2:
                                    restaurant=restaurant["Content"]
                                    restaurant = restaurant[0]
                                    cur=mySQL.connection.cursor()
                                    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(str(idCreator)))
                                    data=cur.fetchall()
                                    data=data[0]
                                    print(restaurant)
                                    print(data)
                                    cur.close()
                                    pk_id=data[0]
                                    usrName=data[3]+" "+data[4]
                                    usrLastName=data[5]
                                    UsrEmail="prueba@gmail.com"
                                    telephone=data[8]
                                    usrIg=data[11]                  
                                    resName=restaurant["name"]
                                    ResIg=restaurant["email"]
                                    print("HOLAAAAAA")
                                    resAddress=restaurant["address"]
                                    #availableChairs=reservation["availableChairs"]
                                    print("QQQQQQQQQQ")
                                    lista2.append([usrName, usrLastName, UsrEmail, telephone, usrIg ,usrIg, resName, ResIg, resAddress, date, hour, ResIg, status, idReservation, pk_id])
                                    #["0 nombre","1 apellido","2 email","3 telefono","4 usuario","5 instagramPerfil",
                                    #"6 restaurante","7 instagramRestaurante","8 direccion","9 fecha","10 hora",
                                    #"11 URL Restaurante","12 estado (Pendiente siempre)","13 Sillas"]
                                    #print(lista1)                        
                                else:
                                    flash("bringAllPostulation Response 2 el API de CRISTIAN 1", "error")    
                            else:
                                flash("bringAllPostulation Fallo el API de CRISTIAN 1", "error")   
                        except Exception as e:
                            print("bringAllPostulation", e)
                        












                else:
                    flash("Response=1 lista2 API Laura", "error")
            else:
                flash("Code 500 Lista2 API Laura", "error")
            print(lista2)           
                        #lista1.append([usrName, usrLastName, UsrEmail, telephone, usrIg ,usrIg, resName, ResIg, resAddress, date, hour, ResIg, status, idReservation, pk_id])

            """
            url="http://"+"159.65.58.193:8000"+"/api/getPublicReservationsWithPaging/666" #esta url cambia por la de Laura
            #me trae mis reservas publicas y privadas que no no han pasado
            #type: 0 privadas, 1 publicas
            lista1=list()
            usrName=None; usrLastName=None; UsrEmail=None; telephone=None; usrIg=None;
            resName=None; ResIg=None; resAddress=None; date=None; hour=None; status=None;
            availableChairs=None; idReservation=None
            try:
                response=requests.get(url, params=None, timeout=5)
                if response.status_code==200:
                    response=response.json()
                    if response["Response"]==2:
                        data=response["Content"]
                        res_final=[len(data)]    #Final reservation with rest name
                        for reservation in data:
                            idRestaurant=reservation["FK_idRestaurant"]
                            url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                            restaurant=requests.get(url, params=None, timeout=5)
                            if restaurant.status_code==200:
                                restaurant=restaurant.json()
                                if response["Response"]==2:
                                    restaurant=restaurant["Content"]
                                    restaurant = restaurant[0]
                                    cur=mySQL.connection.cursor()
                                    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(str(reservation["FK_reservationCreator"])))
                                    data=cur.fetchall(); data=data[0]
                                    cur.close()
                                    #print(reservation)
                                    #print(restaurant)
                                    #print(data)
                                    usrName=data[3]+" "+data[4]
                                    usrLastName=data[5]
                                    UsrEmail="email@email.com"
                                    telephone=data[8]
                                    usrIg=data[11]                  
                                    resName=restaurant["name"]
                                    ResIg=restaurant["email"]
                                    resAddress=restaurant["address"]
                                    date=reservation["reservationDate"]
                                    hour=reservation["reservationHour"]
                                    status="Pendiente"
                                    #availableChairs=reservation["availableChairs"]
                                    idReservation=reservation["PK_idReservation"]
                                    lista1.append([usrName, usrLastName, UsrEmail, telephone, usrIg, resName, ResIg, resAddress, date, hour, status, idReservation])
                                else:
                                    flash("Response 2 el API de CRISTIAN 1", "error")    
                            else:
                                flash("Fallo el API de CRISTIAN 1", "error")   
                    else:
                        flash("Response 2 el API de LAURA 1", "error")    
                else:
                    flash("Fallo el API de LAURA 1", "error")
            except Exception as e:
                print("Erda", e)
            print(lista1)"""





            #Lista 5, son todos los postulantes a mis reservas publicas

            """
            ["PK_idReservation":1,"FK_idDinerU":6,"reservationHour":"23:00","reservationDate":"2019-11-11",
            "FK_idRestaurant":1,"status":1,"firstname":"Veronica","secondname":"Linda",
            "firstLastname":"lo","secondLastname":"lo","igUser":"playboy_col","nameRest":"lo sabroso y lo buenisimo",
            "igRest":"laura.mosquera7"]
            """
            #url="http://159.65.58.193:8000/api/getPostulatesByUserId/"+str(session["PK_IdDiner"])
            url="http://159.65.58.193:8000/api/getPostulatesByUserId/"+str(10)
            tmp=requests.get(url, params=None, timeout=5)
            if tmp.status_code==200:
                tmp=tmp.json()
                print(200)
                if tmp["Response"]==2:
                    print("Response 2")
                    reservation=tmp["Content"]
                    if len(reservation)!=0:
                        lista5_dict=dict()
                        for res in reservation:
                            tmp=[]
                            tmp.append(res["PK_idReservation"]); pk_res=res["PK_idReservation"]
                            tmp.append(res["FK_idDinerU"])
                            tmp.append(res["reservationHour"])
                            tmp.append(res["reservationDate"])
                            name=str(res["firstname"])+" "+res["secondname"]
                            lastName=str(res["firstLastname"])+" "+res["secondLastname"]
                            tmp.append(name)
                            tmp.append(lastName)
                            tmp.append(res["igUser"])
                            tmp.append(res["nameRest"])
                            tmp.append(res["igRest"])
                            if pk_res in lista5_dict:
                                arroz=lista5_dict[pk_res]
                                arroz.append(tmp)
                                lista5_dict[pk_res]=arroz
                            else:
                                lista5_dict[pk_res]=[tmp]
                            
                    else:
                        print("No tiene reservas publicas")
                else:
                    flash("listarPostulantes response 1 API Laura", "error")
            else:
                flash("listarPostulantes error 1 API Laura", "error")
            
            #print(lista5_dict)
            for key in lista5_dict:
                lista5.append(lista5_dict[key])
            
            return render_template("tinder.html",lista1=lista1, lista2=lista2, lista5=lista5)
        else:
            return redirect(url_for('login'))



@login_manager.user_loader
def loadDinerUser(id):
    #print("LOAD", users)
    for user in users:
        if user.id == int(id):
            return user
    return None


@app.route('/logout')
def logout():
    idUser=session["PK_IdUser"]
    session.clear()
    url="http://181.50.100.167:4000/logout?id="+str(idUser)
    try:
        response=requests.post(url, params=None, timeout=5)
        if response.status_code==200:
            session.clear()
            flash("Sesion cerrada Correctamente", "success")
        else:
            flash("Error al cerrar sesion", "error")
    except: 
        flash("logout LAVERDE Error al cerrar sesion", "error")
    
    return redirect(url_for('login'))  #redirect


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = LoginForm()
    if len(users)==0:
        return render_template('forgot_form.html', form=form)
    
    return redirect(url_for('Index'))


@app.route('/botonMembresia', methods=["GET","POST"])
def botonMembresia():    
    if request.method == 'POST':
        id_boton = request.form.get('membresiaBoton')
        #print(id_boton)
    return redirect(url_for('profile'))




























#
#**************************************************************************
#
@app.route('/listarPostulantes')
def listarPostulantes():
    """
    ["PK_idReservation":1,"FK_idDinerU":6,"reservationHour":"23:00","reservationDate":"2019-11-11",
    "FK_idRestaurant":1,"status":1,"firstname":"Veronica","secondname":"Linda",
    "firstLastname":"lo","secondLastname":"lo","igUser":"playboy_col","nameRest":"lo sabroso y lo buenisimo",
    "igRest":"laura.mosquera7"]
    """
    #url="http://159.65.58.193:8000/api/getPostulatesByUserId/"+str(session["PK_IdDiner"])
    url="http://159.65.58.193:8000/api/getPostulatesByUserId/"+str(10)
    tmp=requests.get(url, params=None, timeout=5)
    if tmp.status_code==200:
        tmp=tmp.json()
        print(200)
        if tmp["Response"]==2:
            print("Response 2")
            reservation=tmp["Content"]
            if len(reservation)!=0:
                lista5_dict=dict()
                for res in reservation:
                    tmp=[]
                    tmp.append(res["PK_idReservation"]); pk_res=res["PK_idReservation"]
                    tmp.append(res["FK_idDinerU"])
                    tmp.append(res["reservationHour"])
                    tmp.append(res["reservationDate"])
                    name=str(res["firstname"])+" "+res["secondname"]
                    lastName=str(res["firstLastname"])+" "+res["secondLastname"]
                    tmp.append(name)
                    tmp.append(lastName)
                    tmp.append(res["igUser"])
                    tmp.append(res["nameRest"])
                    tmp.append(res["igRest"])
                    if pk_res in lista5_dict:
                        arroz=lista5_dict[pk_res]
                        arroz.append(tmp)
                        lista5_dict[pk_res]=arroz
                    else:
                        lista5_dict[pk_res]=[tmp]
                    
            else:
                print("No tiene reservas publicas")
        else:
            flash("listarPostulantes response 1 API Laura", "error")
    else:
        flash("listarPostulantes error 1 API Laura", "error")
    
    #print(lista5_dict)
    for key in lista5_dict:
        lista5.append(lista5_dict[key])
    return jsonify(lista5)



@app.route('/botonAceptarPersona')
def botonAceptarPersona():
    """
    se acepta una persona que quiso aplicar a mi reserva.
    Necesito el id del restaurante (res_id),
    necesito el id de la persona   (usr_id) y 
    necesito el status de persona  (status)
    status:
        0 -> pendiente
        1 -> aceptado
        1 -> rechazado
    """

    url="http://159.65.58.193:8000/api/updatePostulatedByReservationIdAndUserId/"+res_id+"/"+usr_id+"/"+status
    response=requests.post(url, params=None, timeout=5)
    if response.status_code==200:
        response=response.json()
        if response["response"]==2:
            if response["content"]==0:
                flash("No se pudo realizar la operacion solicitada", "error")
            elif response["content"]==1:
                flash("No hay sillas disponibles", "error")
            elif response["content"]==2:
                flash("Solicitud actualizada", "success")
            else:
                flash("Ya has rechazado a esta persona, lo sentimos", "error")
        else:
            flash("botonAceparPersona error API Laura 1", "error")
    else:
        flash("botonAceparPersona error API Laura 2", "error")



@app.route('/botonCancelarReserva', methods=["GET","POST"])
def botonCancelarReserva():    
    if request.method == 'POST':
        post_id = request.form.get('delete')
        i=0
        """
        while i in range(len(lista2)):
            if lista2[i][2] == post_id:
                lista2.pop(i)
            i+=1
        """
    return redirect(url_for('tinder'))


@app.route('/botonCheckReserva')
def botonCheckReserva():
    print("INICIO")
    printArray(lista1)
    print("----------")
    printArray(lista2)
    print("############")
    lista2.append(lista1[0])
    reservation=lista1.pop(0)
    printArray(lista1)
    print("----------")
    printArray(lista2)
    print(reservation)
    res_id=str(reservation[13])
    #["0 nombre","1 apellido","2 email","3 telefono","4 usuario","5 instagramPerfil",
    #"6 restaurante","7 instagramRestaurante","8 direccion","9 fecha","10 hora",
    #"11 URL Restaurante","12 estado (Pendiente siempre)","13 Sillas"]
    url="http://159.65.58.193:8000/api/addPostulatedByReservationIdAndUserId/"+res_id+"/"+str(session["PK_IdDiner"])
    print("URL:", url)
    response=requests.post(url, params=None, timeout=5)
    if response.status_code==200:
        response=response.json()
        print("api 200")
        if response["Response"]==2:
            print("Response 2")
            if response["Content"]==1:
                print("Content 1")
                flash("Solicitud enviada correctamente", "success")
            else:
                print("Content 2")
                flash("Ya has enviado esta solicitud", "warning")
        else:
            print("Response 1")
            flash("botonCheckReserva error API Laura 1", "error")
    else:
        print("api error")
        flash("botonCheckReserva error API Laura 2", "error")
    print("FINAL")
    return redirect(url_for('profile'))


@app.route('/botonEquisReserva')
def botonEquisReserva():
    try:
        lista1.pop(0)
    except:
        print("vacia")
    return "nothing"


@app.route('/botonEliminarReserva', methods=["GET","POST"])
def botonEliminarReserva():
    #id_si = str(request.form.get('si'))
    # Me imagino que se puede traer de ahi...
    id_reserva="algo"
    url="http://159.65.58.193:8000/api/deleteReservationByReservationId/"+id_reserva
    response=requests.post(url, params=None)
    if response.status_code==200:
        flash("Reserva eliminada correctamente", "success")
    else:
        flash("botonEliminarReserva error API Laura 2", "error")
    return redirect(url_for('profile'))

@app.route('/botonEditarReserva')
def botonEditarReserva():
    #http://159.65.58.193:8000/api/updateReservation/{idRes}
    """
    Esto me imagino que lo podes hacer en Front, solo es poner el id de la
    reserva que se quiere editar
    """
    idReservation=10
    url="http://159.65.58.193:8000/api/updateReservation/"+str(idReservation)
    return redirect(url)

#
#**************************************************************************
#

























@app.route('/botonPonerReservaPublica', methods=["GET","POST"])
def botonPonerReservaPublica():
    global hReservasActuales
    if request.method == 'POST':
        id_si = str(request.form.get('si'))
        id_no = str(request.form.get('no'))
        i=0
        #http://159.65.58.193:8000/api/updateReservationTypeByReservationId/idReserva

        #print("---> hReservaAcuales",len(hReservasActuales))
        #print("--->", id_si)
        #print("--->", id_no)
        #for r in hReservasActuales:
        #    print(r)

        while i in range(len(hReservasActuales)):
            #print(">",i, hReservasActuales[i][7], id_si, "|", hReservasActuales[i][6])
            if hReservasActuales[i][7] == id_si and hReservasActuales[i][6] =="no":
                hReservasActuales[i][6] = "si"
                id_reserva=str(hReservasActuales[i][7])
                #print("SIIIIIIII", id_reserva)
                url="http://159.65.58.193:8000/api/updateReservationTypeByReservationId/"+id_reserva
                response=requests.post(url, params=None)
                lista3.append(hReservasActuales[i])
            if hReservasActuales[i][7] == id_no and hReservasActuales[i][6] =="si":
                #print("NOOOOOOOO")
                hReservasActuales[i][6] = "no"
                id_reserva=str(hReservasActuales[i][7])
                url="http://159.65.58.193:8000/api/updateReservationTypeByReservationId/"+id_reserva
                response=requests.post(url, params=None)
                j=0
                while j in range(len(lista3)):
                    if lista3[j][7]==id_no:
                        lista3.pop(j)
                    j+=1
            i+=1        
    return redirect(url_for('profile'))


@app.route('/actualizarDatos', methods=["GET","POST"])
def actualizarDatos():
    if request.method == 'POST':
        boton = request.form.get('btn')
        if boton == "aceptar":

            firstName, secondName = " ", " "
            firstLastName, secondLastName = " ", " "

            nombre = request.form.get('nombre'); nombre = nombre.split()
            if len(nombre)>1:
                firstName=str(nombre[0])
                secondName=str(nombre[1]) 
            else:
                firstName=str(nombre[0])

            lastName=request.form.get('apellido'); lastName=lastName.split()
            if len(lastName)>1:
                firstLastName=str(lastName[0])
                secondLastName=str(lastName[1])
            else:
                firstLastName=str(lastName[0])

            
            correo = request.form.get('correo')
            identificacion = request.form.get('identificacion')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            contrasena = request.form.get('contrasena')

            payMethod =""
            infoProfile =""
            igUser = request.form.get('instagram')

            #payMethod
            #infoProfile
            #igUser
            h1=hashlib.sha1(); h1.update(contrasena)
            contrasena=h1; contrasena=str(contrasena.hexdigest())
            #print("contrasena",contrasena)
            if contrasena==session["password"]:
                ############################################ EDIT USER TO DB ############################################
                try:
                    cur=mySQL.connection.cursor()
                    cur.callproc('edit_dinerUser', [session["PK_IdUser"], identificacion, firstName, secondName, firstLastName, secondLastName, direccion, telefono, payMethod, infoProfile, igUser])           
                    mySQL.connection.commit()
                    cur.close()
                    #print("EDITED: ", identificacion, nombre)
                    flash("Informacion editada correctamente", "success")
                except Exception as e:
                    print("+++edit", e)
                    flash("Informacion no editada correctamente", "success")
            else:
                flash("Contrasena incorrecta", "error")

            return redirect(url_for('profile'))
    return "nothing"


@app.route('/cambiarContrasena', methods=["GET","POST"])
def cambiarContrasena():
    if request.method == 'POST':
        boton = request.form.get('btn1')
        if boton == "cambiar":
            contraActual = request.form.get('contraActual')
            contraNueva = request.form.get('contraNueva')
            contraNuevaConf = request.form.get('contraNuevaConf')

            h1=hashlib.sha1(); h1.update(contraActual)
            contraActual=h1; contraActual=str(contraActual.hexdigest())
            if contraActual==session["password"]:
                if contraNueva == contraNuevaConf:
                    h1=hashlib.sha1(); h1.update(contraNueva)
                    contraNueva=h1; contraNueva=str(contraNueva.hexdigest())
                    url="http://181.50.100.167:4000/changePassword?email="+str(session["email"])+"&password="+contraNueva
                    response=requests.post(url, params=None, timeout=5)
                    if response.status_code==200:
                        response=response.json()
                        if response["response"]==2:
                            flash("Contrasena actualizada", "success")
                        else:
                            flash("changePassword API Laverde", "warning")
                    else:
                        flash("changePassword API Laverde", "warning")
                else:
                    flash("Contrasenas deben ser iguales", "warning")
            else:
                flash("Contrasenas vieja no es correcta", "warning")
            return redirect(url_for('profile'))
    return "nothing"


if __name__=='__main__':
    if IP=="159.65.58.193:3000": 
        app.run(port=3000, debug=True, host ='159.65.58.193') #rebug restart all in server
    else:
        app.run(port=3000, debug=True) #rebug restart all local
