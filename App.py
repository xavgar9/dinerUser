IP="127.0.0.1:3000"
#IP="159.65.58.193:3000"
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

@app.route('/registroLaverde/<string:email>/<string:password>', methods=['GET'])
def cambiarContrasena(email, oldPassword, newPassword):
    json=jsonify(Response=2)
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
    print(data)
    #tmp=getUser("", "", "", "", "",data)
    h = hashlib.sha1()
    h.update(data)
    pas=h    
    pas=str(pas.hexdigest())
    json=None
    print("pass:", pas)
    try:
        data=pas
        json=jsonify( Response=2,
                      content=data)
    except Exception as e:
        json=jsonify( Response=1)
        print("+++isVIP", e)
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
@app.route('/')
def Index():
    if "firstName" in session:
        print("INDEX")
        #print(session)
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
    print("DELETED: ",id)
    return redirect(url_for('Index'))   #redirect


#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
@app.route('/login/', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    print("LOGIN")
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
        return redirect(url_for('Index'))
    else:
        print("Inicio")
        if form.validate_on_submit():
            ##############################################################################
            email=request.form['email']
            password=request.form['password']
            print(password)
            h = hashlib.sha1()
            h.update(password)
            pas=h    
            pas=str(pas.hexdigest())
            password=pas
            #user=getUser("", "", "", "", "",password)
            #password=user.password
            print(password)
            #url="http://"+IP+"/loginLaverde/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
            #url="http://181.50.100.167:4000/addUser?userName="+str(userName)+"&email="+str(email)+"&password="+password+"&userType=1"
            url="http://181.50.100.167:4000/login?email="+str(email)+"&password="+str(password)
            #5dc9f2fd91aa3d00a3555d69
            response=requests.post(url, params=None)
            print("Llorelo", response.text)
            
            if response.status_code==200:
                
                response=response.json()                
                print("->",response)

                if response["response"]==2:
                    PK_IdUser=response["content"]["id"]
                    userName=response["content"]["userName"]
                    userType=response["content"]["userType"]
                    try:
                        """
                        print(len(password), password)
                        cur=mySQL.connection.cursor()
                        cur.callproc('login', [email, password])                                        
                        data=cur.fetchall()
                        data=data[0][0]
                        cur.close()
                        print(data)
                        """
                        if True:
                            print("VALIDO LOGIN")
                            #cur=mySQL.connection.cursor()
                            #cur.callproc("getDataDinerUserByEmail", [email])
                            #data=cur.fetchall()                                                        
                            #data=data[0]
                            #cur.close()
                            cur=mySQL.connection.cursor()
                            cur.execute('SELECT * FROM DinerUser WHERE FK_idUser = {0}'.format(PK_IdUser))
                            data=cur.fetchall()
                            print(data)
                            data=data[0]
                            cur.close()
                            print(data)
                            if len(data)!=0:
                                print("DATA mayor a cero")
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
                                session["email"]=email
                                next_page = request.args.get('next')
                                print(session)
                            next_page=None
                            if not next_page or url_parse(next_page).netloc != '':
                                flash("Bienvenido "+ session["firstName"], "success")
                                #userType=3
                                if userType==1:
                                    next_page = url_for('profile')
                                elif userType==2:
                                    return redirect('http://181.50.100.167:3000/?id='+str(session["PK_IdUser"]))
                                else:
                                    return redirect('http://181.50.100.167:4001/Principal/?id='+str(session["PK_IdUser"])+'?pass='+str(password)+'?ciudad=2')








                                                        ########### Tinder ##########################################################
                                global lista1
                                #session["PK_IdDiner"]=1
                                #lista1=[]


                                url="http://"+"181.50.100.167:8000"+"/api/getPublicReservationsWithPaging/666" #esta url cambia por la de Laura
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
                                                        print(data)
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
                                print(lista1)









                            return redirect(next_page)
                        else:
                            flash("Datos incorrectos", "error")
                    except Exception as e:
                        flash("Datos incorrectos", "error")
                        print("+++login", e)                      
        ##############################################################################

    return render_template('login_form.html', form=form)


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    ok=False
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if not ok:
        return redirect(url_for('Index'))
    else:
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
                            user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password)
                            #password=user.password
                            PK_IdUser=str(response["content"]["_id"])
                            print("+++++++++")                
                            print("->", user.data())
                            print("EEEEEEEEE", password)
                            print(PK_IdUser, address, payMethod)
                            userOk=False; emailOk=False
                            try:
                                """                           
                                ### VERIFY EMAIL ###
                                
                                cur=mySQL.connection.cursor()                            
                                cur.callproc('verifyEmail', [email])
                                data=cur.fetchall()
                                data=data[0][0]
                                cur.close()
                                if data==0: emailOk=True
                                ####################

                                ### VERIFY USERNAME ###
                                cur=mySQL.connection.cursor()                            
                                cur.callproc('verifyUserName', [userName])
                                data=cur.fetchall()
                                data=data[0][0]
                                cur.close()
                                if data==0: userOk=True
                                #######################  
                                """                           

                                if True and True:
                                    cur=mySQL.connection.cursor()
                                    cur.callproc('addUser', [PK_IdUser, 1, userName, password, email])                                        
                                    mySQL.connection.commit()
                                    cur.close()

                                    cur=mySQL.connection.cursor()
                                    cur.callproc('add_dinerUser', [PK_IdUser, userName, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod])                                    
                                    mySQL.connection.commit()
                                    cur.close() 
                                    
                                    next_page = request.args.get('next', None)
                                    if not next_page or url_parse(next_page).netloc != '':
                                        next_page = url_for('login')
                                    return redirect(next_page)
                                else:
                                    if not emailOk:
                                        flash("Este email ya esta en uso", "error") 
                                    if not userOk:
                                        flash("Este nombre de usuario ya esta en uso", "error") 
                            except Exception as e:
                                print("+++reg", e)
                        else:
                            print("Response", response["Response"])
                    else:
                        print("error", response.status_code)
                else:
                    flash("La contrasenas no coinciden", "error") 
    return render_template("signup_form.html", form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    ok=False
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if ok:
        return redirect(url_for('login'))   #redirect
    else:
        tmp2 = session
        """
        form1=EditForm()
        form2=PasswordForm()
        print("PROFILE")
        if form1.validate_on_submit():  #cambiar datos general
            if request.method=='POST':
                print("GENERAL")
                numDocument=request.form1['numDocument']
                firstName=request.form1['firstname']
                secondName=request.form1['secondname']
                firstLastName=request.form1['firstlastname']
                secondLastName=request.form1['secondlastname']
                address=request.form1['address']
                telephone=request.form1['telephone']
                payMethod=request.form1['payMethod']
                password=request.form1['password']
                email=request.form1['email']
                instagram=request.form1['instagram']
                #user=getUser("", "", "", "", "",password)
                h1=hashlib.sha1(); h1.update(password)
                password=h1; password=str(password.hexdigest())

                url="http://"+IP+"/loginLaverde/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
                response=requests.get(url, params=None)
                if response.status_code==200:
                    response=response.json()
                    if response["Response"]==2:
                        PK_IdUser=response["content"]["PK_IdUser"]
                        ############################################ EDIT USER TO DB ############################################
                        try:
                            cur=mySQL.connection.cursor()
                            cur.callproc('edit_dinerUser', [numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod])           
                            mySQL.connection.commit()
                            cur.close()
                            print("EDITED: ", numDocument, firstName)
                            flash("Informacion editada correctamente", "success")
                        except Exception as e:
                            print("+++edit", e)
                    else:
                        flash("Datos incorrectos", "error")
            

        elif form2.validate_on_submit():    #cambiar la contrasena
            if request.method=='POST':
                print("CONSTRASENAS")
                password1=request.form2['password1']
                password2=request.form2['password2']
                password3=request.form2['password3']
                if password2==password3:
                    email=session["email"]
                    h1=hashlib.sha1(); h1.update(password1)
                    pas1=h1; pas1=str(pas.hexdigest())

                    h2=hashlib.sha1(); h2.update(password2)
                    pas2=h2; pas2=str(pas.hexdigest())

                    url="http://"+IP+"/cambiarPassLaverde/"+str(email)+"/"+str(pass1)+"/"+str(pass2) #esta url cambia por la de laverde
                    response=requests.get(url, params=None)
                    if response.status_code==200:
                        response=response.json()
                        if response["Response"]==2:
                            flash("Contrasena actualizada", "success")
                        else:
                            flash("Los datos no son validos", "error")
        """
        
        ##########################################################################################################################
        #############################################HISTORIAL DE RESERVAS########################################################
        ##########################################################################################################################
        url="http://"+"181.50.100.167:8000"+"/api/getReservationsRecordByUserId/"+str(session["PK_IdDiner"]) #esta url cambia por la de Laura
        #me trae TODAS las reservas publicas
        print("....",session["PK_IdDiner"])
        historialReservas=list()
        try:
            response=requests.get(url, params=None, timeout=15)
            if response.status_code==200:
                response=response.json()
                print("res", response)
                if response["Response"]==2:
                    data=response["Content"]
                    print("dataaaa", data)
                    for restaurant in data:
                        print(restaurant)
                        idRestaurant=restaurant["FK_idRestaurant"]
                        url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                        tmp=requests.get(url, params=None, timeout=15)
                        if tmp.status_code==200:
                            tmp=tmp.json()
                            if tmp["Response"]==2:
                                tmp=tmp["Content"]
                                individual=list()
                                print(tmp)
                                print(restaurant)
                                individual.append(str(tmp[0]["name"]))
                                individual.append(str(restaurant["reservationDate"]))
                                individual.append(str(restaurant["reservationHour"]))
                                individual.append(str(tmp[0]["address"]))
                                individual.append(str(restaurant["personInCharge"]))

                                historialReservas.append(individual)
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
















        ##########################################################################################################################
        #############################################LISTAR RESERVAS PUBLICAS########################################################
        ##########################################################################################################################
        """
        url="http://"+"181.50.100.167:8000"+"/api/getReservationsRecordByUserId/"+str(session["PK_IdDiner"]) #esta url cambia por la de Laura
        #me trae TODAS las reservas publicas
        try:
            response=requests.get(url, params=None, timeout=5)
            if response.status_code==200:
                response=response.json()
                if response["Response"]==2:
                    data=response["Content"]
                    lista1=list()
                    for restaurant in data:
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

                                lista1.append(individual)
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
        """




        ##########################################################################################################################
        #############################################HISTORIAL DE RESERVAS########################################################
        ##########################################################################################################################

        url="http://181.50.100.167:8000/api/getActiveReservationsByUserIdAndType/"+str(session["PK_IdDiner"])+"/0/" #esta url cambia por la de Laura
        #me trae TODAS las reservas publicas y orivadas actuales de un usuario
        # 0 privada, 1 publica
        hReservasActuales=list()
        try:
            response=requests.get(url, params=None, timeout=15)
            if response.status_code==200:
                response=response.json()
                if response["Response"]==2:
                    data=response["Content"]
                    for restaurant in data:
                        idRestaurant=restaurant["FK_idRestaurant"]
                        url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                        tmp=requests.get(url, params=None, timeout=15)
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

                                hReservasActuales.append(individual)
                            else:
                                flash("privadas Response API de Cristian: 2", "error")
                        else:
                            flash("privadas Fallo el API de Cristian", "error")                            
                else:
                    flash("privadas Fallo el API de LAURA", "error")
            else:
                flash("privadas HTTP error", "error")
        except Exception as e:
            print("+++profile privadas ", e)

        url="http://181.50.100.167:8000/api/getActiveReservationsByUserIdAndType/"+str(session["PK_IdDiner"])+"/1/" #esta url cambia por la de Laura
        try:
            response=requests.get(url, params=None, timeout=15)
            if response.status_code==200:
                response=response.json()
                if response["Response"]==2:
                    data=response["Content"]
                    for restaurant in data:
                        idRestaurant=restaurant["FK_idRestaurant"]
                        url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                        tmp=requests.get(url, params=None, timeout=15)
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

                                hReservasActuales.append(individual)
                            else:
                                flash("publicas Response API de Cristian: 2", "error")
                        else:
                            flash("publicas Fallo el API de Cristian", "error")                            
                else:
                    flash("publicas Fallo el API de LAURA", "error")
            else:
                flash("publicas HTTP error", "error")
        except Exception as e:
            print("+++profile publicas ", e)

    return render_template("profile_view.html", tmp2=tmp2, historialReservas=historialReservas, hReservasActuales=hReservasActuales)
































@app.route('/tinder', methods=['GET', 'POST'])
def tinder():
    global lista1
    ok=False
    #session["PK_IdDiner"]=1
    #lista1=[]
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if ok:
        return redirect(url_for('login'))
    else:
        """url="http://"+"181.50.100.167:8000"+"/api/getPublicReservationsWithPaging/666" #esta url cambia por la de Laura
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
        return render_template("tinder.html",lista1=lista1)



@login_manager.user_loader
def loadDinerUser(id):
    print("LOAD", users)
    for user in users:
        if user.id == int(id):
            return user
    return None


@app.route('/logout')
def logout():
    session.clear()
    flash("Sesion cerrada Correctamente", "success")
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
        print(id_boton)
    return redirect(url_for('profile'))


@app.route('/botonCheckReserva')
def botonCheckReserva():
    #lista2.append(lista1[0])
    #lista1.pop(0)
    return "nothing"

@app.route('/botonEquisReserva')
def botonEquisReserva():
    lista1.pop(0)
    return "nothing"


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


@app.route('/botonPonerReservaPublica', methods=["GET","POST"])
def botonPonerReservaPublica():
    if request.method == 'POST':
        id_si = request.form.get('si')
        id_no = request.form.get('no')
        i=0
        """
        while i in range(len(hReservasActuales)):
            if hReservasActuales[i][8] == id_si and hReservasActuales[i][7] =="No" :
                hReservasActuales[i][7] = "Si"
                lista3.append(hReservasActuales[i])
            if hReservasActuales[i][8] == id_no and hReservasActuales[i][7] =="Si":
                hReservasActuales[i][7] = "No"
                j=0
                while j in range(len(lista3)):
                    if lista3[j][8]==id_no:
                        lista3.pop(j)
                    j+=1
            i+=1
        """
    return redirect(url_for('profile'))


@app.route('/actualizarDatos', methods=["GET","POST"])
def actualizarDatos():
    if request.method == 'POST':
        boton = request.form.get('btn')
        if boton == "aceptar":
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            correo = request.form.get('correo')
            identificacion = request.form.get('identificacion')
            telefono = request.form.get('telefono')
            direccion = request.form.get('direccion')
            contrasena = request.form.get('contrasena')
            
            h1=hashlib.sha1(); h1.update(contrasena)
            contrasena=h1; contrasena=str(contrasena.hexdigest())
            print("contrasena",contrasena)
            url="http://"+IP+"/loginLaverde/"+str(correo)+"/"+str(contrasena) #esta url cambia por la de laverde
            response=requests.get(url, params=None)
            if response.status_code==200:
                response=response.json()
                if response["Response"]==2:
                    PK_IdUser=response["Content"]["PK_IdUser"]
                    ############################################ EDIT USER TO DB ############################################
                    try:
                        cur=mySQL.connection.cursor()
                        cur.callproc('edit_dinerUser', [identificacion, nombre, nombre, apellido, apellido, direccion, telefono, telefono])           
                        mySQL.connection.commit()
                        cur.close()
                        print("EDITED: ", identificacion, nombre)
                        flash("Informacion editada correctamente", "success")
                    except Exception as e:
                        print("+++edit", e)
                else:
                    flash("Datos incorrectos", "error")
            return redirect(url_for('profile'))
    return "nothing"


@app.route('/cambiarContrasenaa', methods=["GET","POST"])
def cambiarContrasenaa():
    if request.method == 'POST':
        boton = request.form.get('btn1')
        if boton == "cambiar":
            contraActual = request.form.get('contraActual')
            contraNueva = request.form.get('contraNueva')
            contraNuevaConf = request.form.get('contraNuevaConf')
            if contraNueva == contraNuevaConf:
                flash("Contrasena Cambiada", "success")
            else:
                flash("Contrasenas deben ser iguales", "warning")
            return redirect(url_for('profile'))
    return "nothing"



if __name__=='__main__':
    if IP=="159.65.58.193:3000": 
        app.run(port=3000, debug=True, host ='159.65.58.193') #rebug restart all in server
    else:
        app.run(port=3000, debug=True) #rebug restart all local
