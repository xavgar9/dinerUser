from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user, logout_user, login_user, login_required
from werkzeug.urls import url_parse
from forms import SignupForm, LoginForm, EditForm, PasswordForm
from datetime import timedelta
import requests
import hashlib
"""
Clasificacion VIP
"""
"""
####
#CREAR VIP
procedure createVIPMembership(IN idComensal INT, IN fechaCorte DATE)
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
####

####
#ELIMINAR VIP
DeleteMembership(IN IdDiner)
####

####
#ELIMINAR CUENTA USUARIO
session["PK_IdDiner"]
####
"""
"""
LISTAR EL HISTORIAL DE RESERVAS DE UN USUARIO
"""
session=dict()
session["PK_IdDiner"]="1"
url="http://"+"181.50.100.167:8000"+"/api/getReservationsRecordByUserId/"+session["PK_IdDiner"] #esta url cambia por la de Laura
#me trae TODAS las reservas publicas
historialReservas=list()
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
                        #print(tmp)
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
print(historialReservas)