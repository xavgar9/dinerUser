IP="127.0.0.1:3000"
#IP="159.65.58.193:3000"

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
    data=data[0]
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
    data=tmp

    json=None
    try:
        data=data[0]
        json=jsonify( Response=2,
                      Content=data)
    except:
	    json=jsonify(Response=1)
    return json


@app.route('/isVIP/<string:id>/', methods=['GET'])
def isVIP(id):
    id=int(id)
    json=None
    try:
        cur=mySQL.connection.cursor()
        cur.callproc('idDinerUser', [id])
        data=cur.stored_results()
        json=jsonify( Response='1',
                      content=data[0])
    except Exception as e:
        json=jsonify( Response='2',
                      content=e)
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
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if not ok:
        return redirect(url_for('Index'))
    else:
        if form.validate_on_submit():
            ##############################################################################
            email=request.form['email']
            password=request.form['password']
            user=getUser("", "", "", "", "",password)
            #password=user.password

            url="http://"+IP+"/loginLaverde/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
            response=requests.get(url, params=None)
            if response.status_code==200:
                response=response.json()
                if response["Response"]==2:
                    PK_IdUser=response["Content"]["PK_IdUser"]
                    userName=response["Content"]["userName"]
                    try:
                        print(len(password), password)
                        cur=mySQL.connection.cursor()
                        cur.callproc('login', [email, password])                                        
                        data=cur.fetchall()
                        data=data[0][0]
                        cur.close()
                        if data==1:
                            print("VALIDO LOGIN")
                            cur=mySQL.connection.cursor()
                            cur.callproc("getDataDinerUserByEmail", [email])
                            data=cur.fetchall()                                                        
                            data=data[0]
                            cur.close()
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
                    
                        next_page=None
                        
                        """
                        if user is not None:
                            login_user(user) 
                            users.append(user)        
                            try:
                                
                                #cur=mySQL.connection.cursor()
                                #cur.callproc('getDinerIdByIdUser', [PK_IdUser])
                                #mySQL.connection.commit()
                                #session["PK_IdDiner"]=str(cur.stored_results())
                                
                                session["PK_IdDiner"]="1"
                            except Exception as e:
                                print("+++ Error al recuperar IdDiner", e)
                            session["PK_IdUser"]=PK_IdUser
                            session["firstName"]=firstName
                            session["secondName"]=secondName
                            session["lastName"]=lastName
                            session["telephone"]=telephone
                            session["email"]=email    
                            session["userName"]=userName                    
                            
                            next_page = request.args.get('next')
                        """
                        if not next_page or url_parse(next_page).netloc != '':
                            flash("Bienvenido "+ session["firstName"], "success")
                            next_page = url_for('profile')
                        return redirect(next_page)
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
                    user=getUser("", "", "", "", "",password)
                    password=user.password
                    url="http://"+IP+"/registroLaverde/"+str(userName)+"/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
                    response=requests.get(url, params=None)
                    if response.status_code==200:
                        response=response.json()
                        if response["Response"]==2:
                            address=" "; payMethod=" "
                            user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password)
                            password=user.password
                            PK_IdUser=str(response["content"]["PK_User"])
                            print("+++++++++")                
                            print("->", user.data())
                            print("EEEEEEEEE", password)
                            print(PK_IdUser, address, payMethod)
                            userOk=False; emailOk=False
                            try:                           
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

                                if emailOk and userOk:
                                    cur=mySQL.connection.cursor()
                                    cur.callproc('addUser', [1, userName, password, email])                                        
                                    mySQL.connection.commit()
                                    cur.close()

                                    cur=mySQL.connection.cursor()
                                    cur.callproc('add_dinerUser', [userName, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod])                                    
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
        tmp = session
        form1=EditForm()
        form2=PasswordForm()
        print("PROFILE")
        if form1.validate_on_submit():
            if request.method=='POST':
                print("GENERAL")
                numDocument=request.form1['numDocument']
                firstName=request.form1['firstname']
                secondName=request.form1['secondname']
                firstLastName=request.form1['firstLastname']
                secondLastName=request.form1['secondLastname']
                address=request.form1['address']
                telephone=request.form1['telephone']
                payMethod=request.form1['payMethod']
                password=request.form1['password']
                email=request.form1['email']
                user=getUser("", "", "", "", "",password)
                password=user.password

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

        elif form2.validate_on_submit():
            if request.method=='POST':
                print("CONSTRASENAS")
                password1=request.form2['password1']
                password2=request.form2['password2']
                password3=request.form2['password3']
                if password2==password3:
                    email=session["email"]
                    user=getUser("", "", "", "", "",password1)
                    password1=user.password
                    user=getUser("", "", "", "", "",password2)
                    password2=user.password
                    url="http://"+IP+"/cambiarPassLaverde/"+str(email)+"/"+str(password1)+"/"+str(password2) #esta url cambia por la de laverde
                    response=requests.get(url, params=None)
                    if response.status_code==200:
                        response=response.json()
                        if response["Response"]==2:
                            flash("Contrasena actualizada", "success")
                        else:
                            flash("Los datos no son validos", "error")
    return render_template("profile_view.html", form1=form1, form2=form2, tmp=tmp)


@app.route('/tinder', methods=['GET', 'POST'])
def tinder():
    ok=False
    session["PK_IdDiner"]=1
    try:
        print(session["PK_IdDiner"])
    except KeyError:
        ok=True
    if ok:
        return redirect(url_for('login'))
    else:
        res_final=None

        ###
        #   Lista las reservas publicas del usuario PK_IdDiner
        ###
        dic=dict()

        #1 no funciona
        #2 funciona

        url="http://"+"181.50.100.167:8000"+"/api/getActiveReservationsByUserIdAndType/"+str(session["PK_IdDiner"])+"/1" #esta url cambia por la de Laura
        #me trae mis reservas publicas y privadas que no no han pasado
        #type: 0 privadas, 1 publicas
        print("Arroz")
        response=requests.get(url, params=None)
        print("Con pollo")
        if response.status_code==200:
            response=response.json()
            if response["Response"]==2:
                data=response["Content"]
                #print("Reservas publicas activas: ", data)
                res_final=[len(data)]    #Final reservation with rest name
                for reservation in data:
                    idRestaurant=reservation["FK_idRestaurant"]
                    url="http://"+"181.50.100.167:5000"+"/getRestaurant/"+str(idRestaurant)
                    tmp=requests.get(url, params=None)
                    if tmp.status_code==200:
                        tmp=tmp.json()
                        if response["Response"]==2:
                            tmp=tmp["Content"]
                            print()
                            print()
                            print()
                            print(tmp)
                            print()
                            print(reservation["PK_idReservation"])
                            print()
                            erda=[]  
                            erda.append(str(tmp[0]["name"]))
                            erda.append(str(tmp[0]["email"]))
                            erda.append(str(tmp[0]["address"]))
                            erda.append(str(reservation["reservationDate"]))
                            erda.append(str(reservation["reservationHour"]))
                            erda.append(str(reservation["availableChairs"]))
                            dic[reservation["PK_idReservation"]]=erda
                                                                  #nombre del restaurante
                                                                  #ig del usuario
                                                                  #fecha de la reserva
                                                                  #hora de la reserva
                                                                  #sillas disponibles
                        else:
                            flash("Response: 1", "error")
                            print("*** Response: 0")
                    else:
                        flash("Cristian Status code:"+str(tmp.status_code), "error")
                        print("*** Cristian Status code:"+str(tmp.status_code), data)
                #else:
                #    flash("No trajo nada el API de LAURA", "error")
                #    print("*** No trajo nada el API de LAURA", data)
            else:
                flash("Fallo el API de LAURA", "error")
        else:
            flash("Laura Status code:"+str(response.status_code), "error")
            print("*** Laura Status code:"+str(response.status_code), url)
        

                            #res_final.append([str(tmp["name"]), str(tmp["email"]), str(reservation["reservationDate"]), str(reservation["reservationHour"])])
                                                  #nombre del restaurante
        ###
          #
        ###


        ###
        #   Lista los usuarios que estan aplicando a una reserva del usuario PK_IdDiner
        ###
        usr_final=[]
        print("*********************************************************************************************")
        for idReservation in dic.keys():
            url="http://181.50.100.167:8000/api/getPostulatesByReservationId/"+str(idReservation) #esta url cambia por la de Laura
            response=requests.get(url, params=None)
            if response.status_code==200:
                response=response.json()
                print()
                print()
                print()
                print()
                print("RESPONSE:", response)
                if response["Response"]==2:
                    data=response["Content"]
                    for usr in data:
                        usrName=""
                        usrIgUser=""
                        usrInfo=""
                        usrStatus=None

                        cur=mySQL.connection.cursor()
                        print("FK_idUserU", usr["FK_idUserU"])
                        cur.callproc("getUserByIdUser", [usr["FK_idUserU"]])
                        data2=cur.fetchall()                                
                        data2=data2[0]
                        cur.close()
                        if len(data)!=0:
                            usrName=str(data2[3])+" "+str(data2[4])+" "+str(data2[5])
                            usrIgUser=data[11]
                            usrInfo=data[10]

                        if usr["status"]==1:
                            usrStatus="Pendiente"
                        elif usr["status"]==2: 
                            usrStatus="Aceptado"
                        else:
                            usrStatus="Rechazado"
                        
                        tmp=dic[idReservation]
                        tmp.append(usrName)
                        tmp.append(usrIgUser)
                        tmp.append(usrInfo)
                        tmp.append(usrStatus)
                        dic[idReservation]=tmp
            else:
                #esto es temporal porque Veronica no quiere llenar sus tablas con datos
                print("VACIO getPostulatesByReservationId")
                tmp=dic[idReservation]
                tmp.append("usrName EPA")
                tmp.append("usrIgUser EPA")
                tmp.append("usrInfo EPA")
                tmp.append("usrStatus EPA")
                dic[idReservation]=tmp
        ###
          #
        ###
        """
        [0] str(tmp["name"])
        [1] str(tmp["email"])
        [2] str(tmp["address"]) 
        [3] str(reservation["reservationDate"])
        [4] str(reservation["reservationHour"]) 
        [5] str(reservation["avaibleChairs"])]
        [6] append(usrName)
        [7] append(usrIgUser)
        [8] append(usrInfo)
        [9] append(usrStatus)
        """

        


        #print(res_final)
        #print(usr_final)
        print(dic)
        lista1=[]
        for idReservation in dic.keys():
            print()
            print("le dict", dic)
            resName=dic[idReservation][0]
            usrName=dic[idReservation][6]
            date=dic[idReservation][3]
            hour=dic[idReservation][4]
            status=dic[idReservation][9]
            resIgUser="tdt_hamburguesas" #dic[idReservation][1]
            usrIgUser=dic[idReservation][7]
            lista1.append([resName, usrName, date, hour, status, resIgUser, usrIgUser])
        """
        lista1 = [["Mr. Wings","Carol","10/11/2019","09:30 p.m","Pendiente","misterwings","carol_alt"],
                  ["Martha","William","11/12/2019","10:30 p.m","Activo","americanpizzakw","williamaguirrezapata"],
                  ["3 x mil","Xavi","11/12/2019","10:30 p.m","Pendiente","hamburguerperfeito","pedromorrot"],
                  ["Warner","Alexa","11/12/2019","10:30 p.m","Activo","alitastogo","om7sein_"]]
        """

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



if __name__=='__main__':
    if IP=="159.65.58.193:3000": 
        app.run(port=3000, debug=True, host ='159.65.58.193') #rebug restart all in server
    else:
        app.run(port=3000, debug=True) #rebug restart all local