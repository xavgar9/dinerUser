#IP="127.0.0.1:3000"
IP="159.65.58.193:3000"

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
app.config['MYSQL_HOST']='localhost' #data base ubication -> localhost
app.config['MYSQL_USER']='admin' #-> admin
app.config['MYSQL_PASSWORD']='3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2' #->3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2
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
    json=jsonify(status='1',
                 content=data)
    return json

@app.route('/registroLaverde/<string:userName>/<string:email>/<string:password>', methods=['GET'])
def registroLaverde(userName, email, password):
    data={"PK_User": 2}
    #data=(userName, email, password)
    json=jsonify(status='1',
                 content=data)
    return json

@app.route('/registroLaverde/<string:email>/<string:password>', methods=['GET'])
def cambiarContrasena(email, oldPassword, newPassword):
    json=jsonify(status='1')
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
    json=jsonify(status='1',
                 content=data)
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
    json=jsonify(status='1',
                 content=data)
    return json

@app.route('/getRestaurantNameById/<string:restaurantId>', methods=['GET'])
def getRestaurantNameById(restaurantId):
    data=""
    if restaurantId=="1"    :
        data="Warner Foods"
    else:
        data="Salchiburguer"
    json=jsonify(status='1',
                 content=data)
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
         "payMethod": data[9]}
    data=tmp

    json=None
    try:
        data=data[0]
        json=jsonify( status='1',
                      content=data)
    except:
	    json=jsonify(status='0')
    return json


@app.route('/isVIP/<string:id>/', methods=['GET'])
def isVIP(id):
    id=int(id)
    json=None
    try:
        cur=mySQL.connection.cursor()
        cur.callproc('idDinerUser', [id])
        data=cur.stored_results()
        json=jsonify( status='1',
                      content=data[0])
    except Exception as e:
        json=jsonify( status='2',
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
                if response["status"]=='1':
                    PK_IdUser=response["content"]["PK_IdUser"]
                    userName=response["content"]["userName"]
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
                        if response["status"]=='1':
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
                    if response["status"]=='1':
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
                        if response["status"]=='1':
                            flash("Contrasena actualizada", "success")
                        else:
                            flash("Los datos no son validos", "error")
    return render_template("profile_view.html", form1=form1, form2=form2, tmp=tmp)


@app.route('/tinder', methods=['GET', 'POST'])
def tinder():
    ok=False
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

        url="http://"+IP+"/getPostulatedReservationByUserId/"+str(session["PK_IdDiner"]) #esta url cambia por la de laverde
        response=requests.get(url, params=None)
        if response.status_code==200:
            response=response.json()
            if response["status"]=='1':
                data=response["content"]
                res_final=[len(data)]    #Final reservation with rest name
                for reservation in data:
                    idRestaurant=reservation["FK_idRestaurant"]
                    url="http://"+IP+"/getRestaurantNameById/"+str(idRestaurant)
                    tmp=requests.get(url, params=None)
                    if tmp.status_code==200:
                        tmp=tmp.json()
                        if response["status"]=='1':
                            res_final.append([str(tmp["content"]), str(reservation["reservationDate"]), str(reservation["reservationHour"])])
        ###
          #
        ###

        ###
        #   Lista los usuarios que estan aplicando a una reserva del usuario PK_IdDiner
        ###
        usr_final=[]
        url="http://"+IP+"/getPostulatedByReservationId/"+str(session["PK_IdDiner"]) #esta url cambia por la de laverde
        response=requests.get(url, params=None)
        if response.status_code==200:
            response=response.json()
            if response["status"]=='1':
                data=response["content"]
                usr_final=[len(data)] 
                for usr in data:
                    name=session["firstName"]; igUser=session["igUser"]
                    if name!=None and igUser!=None:
                        status=None
                        if usr["status"]==1: status="Stand By"
                        else: status="Accepted"                  
                        usr_final.append([usr["PK_idUser"], name, igUser, status])

        ###
          #
        ###

          


        print(res_final)
        print(usr_final)


        return render_template("tinder.html")
"""

@app.route('/tinder', methods=['GET', 'POST'])
def tinder():
    return render_template("tinder.html")"""

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