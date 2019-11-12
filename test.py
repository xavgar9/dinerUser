from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm, EditForm, PasswordForm
from datetime import timedelta
import requests
import hashlib
app=Flask(__name__) #web service

############################################ MYSQL CONNECTION ############################################

app.config['MYSQL_HOST']='localhost' #data base ubication -> localhost
app.config['MYSQL_USER']='root' #-> admin
app.config['MYSQL_PASSWORD']='' #->3ad853f1abc94a67dc9ceed07547d5aa6dd5ce129611feb2
app.config['MYSQL_DB']='dinerUser' #data base name -> dinerUser

app.secret_key=' srguM44wgw45gewregkujfxhgzdgAHqgreggwwerigpewergWwERwrPegQ#$dgvsdgrLla%wg%Q24g5"vEssFDVSEv3Cr3t4SDFewr4tgsfdbvsd'
login_manager=LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


mySQL=MySQL(app)   #data base connection
app.run(port=3000, debug=True)



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
                        cur=mySQL.connection.cursor()
                        cur.execute('SELECT * FROM DinerUser WHERE PK_idDiner = {0}'.format(str(reservation["FK_reservationCreator"])))
                        data=cur.fetchall(); data=data[0]
                        cur.close()
                        print(reservation)
                        print(restaurant)
                        print(data)
                        usrName=data[3]+data[4]
                        usrLastName=data[5]+data[6]
                        UsrEmail="email@email.com"
                        telephone=data[8]
                        usrIg=data[11]                  
                        resName=restaurant["name"]
                        ResIg=restaurant["email"]
                        resAddress=restaurant["address"]
                        date=reservation["reservationDate"]
                        hour=reservation["reservationHour"]
                        status="Pendiente"
                        availableChairs=reservation["availableChairs"]
                        idReservation=reservation["idReservation"]
                        lista1.append([usrName, usrLastName, UsrEmail, telephone, usrIg, resName, ResIg, resAddress, date, hour, status, availableChairs, idReservation])
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

