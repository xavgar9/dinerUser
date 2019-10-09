############################################ name ############################################
##########################################################################################################
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__) #web service

############################################ MYSQL CONNECTION ############################################
app.config['MYSQL_HOST']='localhost' #data base ubication
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root' 
app.config['MYSQL_DB']='userDiner' #data base name

mySQL=MySQL(app)   #data base connection
##########################################################################################################

################################################ SETTINGS ################################################
app.secret_key=' suPerLlavE'
##########################################################################################################


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/add_dinerUser', methods=['POST'])
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

        """
        ############################################ ADD USER TO DB ############################################
        cur=mySQL.connection.cursor()
        cur.execute('CALL add_dinerUser(numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod)',
                    (numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod))
        mySQL.connection.commit()
        flash('User Added Succesfully')
        """
        flash('User Added Succesfully')
        #print(numDocument, firstname)
        return redirect(url_for('Index'))   #redirect


@app.route('/edit_dinerUser/<string:id>')
def get_dinerUser(id):
    """
    cur=mySQL.connection.cursor()
    cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    data=cur.fetchall()
    """
    tmp=(1,1453487801,'pedro','pablo','leon','jaramillo','cra 44 #13-10',8295562,'tarjeta de credito')
    data=[tmp]
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

        """
        cur=mySQL.connection.cursor()
        cur.execute('CALL edit_dinerUser(numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod)'
                    (numDocument, firstname, secondname, firstLastname, secondLastname, address, telephone, payMethod))
        mySQL.connection.commit()
        flash('User Added Succesfully')
        """
        print(data)
    return redirect(url_for('Index'))   #redirect

@app.route('/delete_dinerUser/<string:id>')
def delete_dinerUser(id):
    """
    cur=mySQL.connection.cursor()
    cur.execute('DELETE FROM DinerUser WHERE PK_idDiner = {0}'.format(id))
    mySQL.connection.commit()
    flash('User Added Succesfully')
    """
    flash('User Deleted Succesfully')
    return redirect(url_for('Index'))   #redirectna
if __name__=='__main__':
    app.run(port=3000, debug=True) #rebug restart all
