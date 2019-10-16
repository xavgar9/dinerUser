#request.json['name'] para recibir y usar json de otras paginas
#pip install flask
#pip install flask-mysql
#pip install flask-login
#pip install Flask-WTF

############################################ name ############################################
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, logout_user, login_user
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm



from reservation import reservation
from models import dinerUser, users

app=Flask(__name__) #web service

############################################ MYSQL CONNECTION ############################################
app.config['MYSQL_HOST']='localhost' #data base ubication
app.config['MYSQL_USER']='admin'
app.config['MYSQL_PASSWORD']='3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2' 
app.config['MYSQL_DB']='dinerUser' #data base name

mySQL=MySQL(app)   #data base connection
##########################################################################################################

################################################ SETTINGS ################################################
app.secret_key=' suPerLlavE'
login_manager=LoginManager(app)
login_manager.login_view = "login"
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
        json=jsonify( idUser=id,
                  numDocument=data[1],
                  firstname=data[2],
                  secondname=data[3],
                  firstLastname=data[4],
                  secondLastname=data[5],
                  address=data[6],
                  telephone=data[7],
                  payMethod=data[8],
                  status='1')
    except:
	json=jsonify(status='0')
    return json

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/add_dinerUser/', methods=['POST'])
def add_dinerUser():
    if request.method == 'POST':
        numDocument=request.form['numDocument']
        firstname=request.form['firstname']
        secondname=request.form['secondname']
        firstLastname=request.form['firstLastname']
        secondLastname=request.form['secondLastname']
        address=request.form['address']
        telephone=request.form['telephone']
        payMethod=request.form['payMethod']

        
        ############################################ ADD USER TO DB ############################################
        cur=mySQL.connection.cursor()
        cur.execute('CALL add_dinerUser(numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod)',
                    (numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod))
        mySQL.connection.commit()
        #flash('User Added Succesfully')
        
        flash('User Added Succesfully')
        print(numDocument, firstname)
        return redirect(url_for('Index'))   #redirect


@app.route('/edit_dinerUser/<string:id>')
def get_dinerUser(id):
    
    cur=mySQL.connection.cursor()
    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    data=cur.fetchall()
    
    #tmp=(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito')
    #data=[tmp]
    #print(data)
    return render_template('editDinerUser.html', contact=data[0])

@app.route('/edit_dinerUser/<string:id>')
def edit_dinerUser():
    if request.method=='POST':
        numDocument=request.form['numDocument']
        firstname=request.form['firstname']
        secondname=request.form['secondname']
        firstLastname=request.form['firstLastname']
        secondLastname=request.form['secondLastname']
        address=request.form['address']
        telephone=request.form['telephone']
        payMethod=request.form['payMethod']

        
        cur=mySQL.connection.cursor()
        cur.execute('CALL edit_dinerUser(numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod)'
                    (numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod))
        mySQL.connection.commit()
        flash('User Edited Succesfully')
        
        #print(data)
    return redirect(url_for('Index'))   #redirect

@app.route('/delete_dinerUser/<string:id>')
def delete_dinerUser(id):
    
    cur=mySQL.connection.cursor()
    cur.execute('DELETE FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    mySQL.connection.commit()
    flash('User Added Succesfully')
    
    #flash('User Deleted Succesfully')
    return redirect(url_for('Index'))   #redirect



#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
#Codigo tomado de: https://j2logo.com/tutorial-flask-leccion-4-login/
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('Index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('Index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = dinerUser(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('Index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)
    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('Index'))  #redirect

@login_manager.user_loader
def load_dinerUser(id):
    for user in users:
        if user.id == int(id):
            return user
    return None

if __name__=='__main__':
    app.run(port=3000, debug=True, host ='159.65.58.193') #rebug restart all
