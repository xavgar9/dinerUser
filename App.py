#request.json['name'] para recibir y usar json de otras paginas
#pip install flask
#pip install flask-mysql
#pip install flask-login
#pip install Flask-WTF
#pip install requests

############################################ name ############################################
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, logout_user, login_user
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm
import requests



from reservation import reservation
from models import DinerUser, users, get_user

app=Flask(__name__) #web service

############################################ MYSQL CONNECTION ############################################
app.config['MYSQL_HOST']='localhost' #data base ubication -> localhost
app.config['MYSQL_USER']='admin' #-> admin
app.config['MYSQL_PASSWORD']='3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2' #->3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2
app.config['MYSQL_DB']='dinerUser' #data base name -> dinerUser

mySQL=MySQL(app)   #data base connection
##########################################################################################################

################################################ SETTINGS ################################################
app.secret_key=' suPerLlavE'
login_manager=LoginManager(app)
login_manager.login_view = "login"
##########################################################################################################




##########################################################################################################
##########################################################################################################
##################################APIS TEMPORALES DE OTROS MODULOS########################################
##########################################################################################################
##########################################################################################################
@app.route('/loginLaverde/<string:email>/<string:password>', methods=['GET'])
def loginLaverde(email,password):
    data={"existe": 1}
    json=jsonify(status='1',
                 content=data)
    return json

@app.route('/registroLaverde/<string:userName>/<string:email>/<string:password>', methods=['GET'])
def registroLaverde(userName, email, password):
    data={"PK_User": 1}
    #data=(userName, email, password)
    json=jsonify(status='1',
                 content=data)
    return json



##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

@app.route('/edit_dinerUserJson/<string:id>', methods=['GET'])
def get_dinerUserJson(id):
    cur=mySQL.connection.cursor()
    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    data=cur.fetchall()
    #data=(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito')
    print(data)
    json=None
  
    try:
        data=data[0]
        json=jsonify( status='1',
                      content=data)
    except:
	    json=jsonify(status='0')
    return json


@app.route('/chantateTuVIP/<string:id>', methods=['GET'])
def chantateTuVIP(id):
    #cursor.stored_results()
    pass

@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/edit_dinerUser/<string:id>')
def edit_dinerUser(id):
    if request.method=='POST':
        numDocument=request.form['numDocument']
        firstName=request.form['firstname']
        secondName=request.form['secondname']
        firstLastName=request.form['firstLastname']
        secondLastName=request.form['secondLastname']
        address=request.form['address']
        telephone=request.form['telephone']
        payMethod=request.form['payMethod']

        ############################################ EDIT USER TO DB ############################################
        try:
            cur=mySQL.connection.cursor()
            cur.execute('CALL edit_dinerUser({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})'.format(
                        id, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod))
            mySQL.connection.commit()
            #flash('User Edited Succesfully')
            print("EDITED: ", numDocument, firstName)
        except Exception as e:
            print("+++edit", e)
        ############################################ EDIT USER TO DB ############################################

    return redirect(url_for('Index'))   #redirect

@app.route('/delete_dinerUser/<string:id>')
def delete_dinerUser(id):
    ############################################ DELETE USER TO DB ############################################
    try:
        cur=mySQL.connection.cursor()
        cur.callproc('delete_dinerUser', [id])
        mySQL.connection.commit()
    except Exception as e:
        print("+++del", e)
    ############################################ DELETE USER TO DB ############################################

    flash('User Deleted Succesfully')
    print("DELETED: ",id)
    return redirect(url_for('Index'))   #redirect


#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
@app.route('/login/', methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('Index'))
    form = LoginForm()
    if form.validate_on_submit():
        ##############################################################################
        email=request.form['email']
        password=request.form['password']
        url="http://127.0.0.1:3000/loginLaverde/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
        response=requests.get(url, params=None)
        if response.status_code==200:
            response=response.json()
            if response["status"]=='1':
                user=get_user(email,password)
                if user is not None and user.check_password(str(password)):
                    login_user(user, remember=False)
                    next_page = request.args.get('next')
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('Index')
                    return redirect(next_page)
        ##############################################################################
    return render_template('login_form.html', form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('Index'))
    form = SignupForm()
    if form.validate_on_submit():
        """
        name=form.name.data
        email=form.email.data
        password=form.password.data
        """
    
        if request.method == 'POST':
            numDocument=request.form['numDocument']
            name=request.form['name']
            firstName, secondName=map(str,name.split())
            lastName=request.form['lastName']
            firstLastName, secondLastName=map(str,lastName.split())
            #address=request.form['address']
            telephone=request.form['telephone']
            #payMethod=request.form['payMethod']
            userName=request.form['userName']
            email=request.form['email']
            password=request.form['password']
            password2=request.form['password2']

            if password==password2:
                ############################################ ADD USER TO DB ############################################
                """
                Aqui va el API de anderson que me da PK del usuario dado el 
                nombre de usuario "_id" (string)
                """
                url="http://127.0.0.1:3000/registroLaverde/"+str(userName)+"/"+str(email)+"/"+str(password) #esta url cambia por la de laverde
                response=requests.get(url, params=None)
                if response.status_code==200:
                    response=response.json()
                    if response["status"]=='1':
                        address=" "; payMethod=" "
                        user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password)
                        password=user.password
                        PK_IdUser=str(response["content"]["PK_User"])
                        print("+++++++++")                
                        print(user)
                        print(PK_IdUser, address, payMethod)
                        try:
                            """
                            cur=mySQL.connection.cursor()
                            cur.callproc('add_dinerUser', [userName, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod])
                            #cur.callproc('add_dinerUser', [PK_IdUser, userName, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod])
                            mySQL.connection.commit()
                            """
                            print("ADDED:", numDocument, userName)
                            login_user(user, remember=True)
                            next_page = request.args.get('next', None)
                            if not next_page or url_parse(next_page).netloc != '':
                                next_page = url_for('Index')
                            return redirect(next_page)
                        except Exception as e:
                            print("+++reg", e)
                else:
                    flash("La contrasenas no coinciden") 


                """
                PK_IdUser=1
                address="Direccion"
                payMethod="payMethod"
                user=None
                userName=str(userName); address=str(address); telephone=str(telephone)
                try:
                    print(1)
                    cur=mySQL.connection.cursor()
                    print(2)
                    user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password)
                    print(3)
                    password=user.password
                    print(4)
                    cur.callproc('add_dinerUser', [userName, numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod])
                    print(5)
                    mySQL.connection.commit()
                    print(6)
                    #flash('User Added Succesfully')
                    users.append(user)
                    
                    print("ADDED:", numDocument, userName)
                except Exception as e:
                    print("+++reg", e) 
                ############################################ ADD USER TO DB ############################################
                # Creamos el usuario y lo guardamos
                #user = dinerUser(len(users) + 1, name, email, password)
                #users.append(user)
                # Dejamos al usuario logueado
                #user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password, False)
                user=DinerUser(numDocument, firstName, secondName, firstLastName, secondLastName, address, telephone, payMethod, email, userName, password)
                login_user(user, remember=True)
                next_page = request.args.get('next', None)
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('Index')
                return redirect(next_page)
            else:
                flash('Las contrasenas no coinciden')
                """
    return render_template("signup_form.html", form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('Index'))  #redirect

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """
    if current_user.is_authenticated:
        return redirect(url_for('Index'))"""
    form = LoginForm()
    """if form.validate_on_submit():
        user = get_user(request.form['email'])
        print(user)
        if user is not None and user.check_password(request.form['password']):
            print("LOGIN AQUI")
            login_user(user, remember=False)
            print("LOGIN ALLA")
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('Index')
            return redirect(next_page)"""
    return render_template('forgot_form.html', form=form)
    #return redirect('forgot_form.html')
    #return render_template("forgot_form.html", form=form)  #redirect


@login_manager.user_loader
def load_dinerUser(id):
    for user in users:
        if user.id == int(id):
            return user
    return None

if __name__=='__main__':
    app.run(port=3000, debug=True) #rebug restart all local
    #app.run(port=3000, debug=True, host ='159.65.58.193') #rebug restart all in server