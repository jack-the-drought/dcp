import subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib,sys
import datetime
from flask import Flask, request, render_template,flash,url_for, redirect, session, abort ,g
from newsavedata import *
from getnewaddr import getnewaddress
from finaldatabase import db
from finaldatabase import tr_list,User
from flask.ext.login import login_user , logout_user , current_user , login_required, LoginManager, AnonymousUserMixin
import hashlib
from getdata import *

login_manager = LoginManager()
app = Flask(__name__)
app.secret_key = 'xxxxyyyyyzzzzz'
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(idd):
	return User.query.filter_by(id=idd).first()

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['email'],request.form['password'])
    db.session.add(user)
    db.session.commit()
    flash('Utilisateur enregistre avec succes')
    time.sleep(1)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	username = request.form['username']
	password = request.form['password']
	password = hashlib.md5(password).digest().encode("hex")
	reguser = User.query.filter_by(name=username,password=password).first()
        if reguser is None:
            error = 'Utilisateur ou mot de passe invalide, veuillez ressayer.'
        else:
	    #print request.args.get('next')
	    login_user(reguser)
		#redirect to list transactions	    
            return redirect(request.args.get('next') or url_for('listtransactions',id = reguser.id))
    return render_template('login.html', error=error)

@app.route('/listtransactions/<id>',methods=['GET','POST'])
@login_required
def listtransactions(id):
#require the login here and in bobapp clone
	transactions = tr_list.query.filter_by(owner_id=id)
	return render_template("listtransactions.html",transactions = transactions)

@app.route("/")
def index():
	return render_template("newspindex.html")

@app.route("/newsavehash/<hashh>")
def savethehash(hashh):
	new_address = getnewaddress()
	#here add the owner id using curret_user.id
	#print current_user
	#print current_user.__class__
	#print current_user.__class__.__name__
	if current_user.is_authenticated:
		new_tr = tr_list(hashh+str(int(time.time())),new_address,0,"blanko",current_user.id)
	else:
		new_tr = tr_list(hashh+str(int(time.time())),new_address,0,"blanko")
	db.session.add(new_tr)
	db.session.commit()
	
	return render_template("confirmbtn.html",hash=hashh,addr = new_address)
	


@app.route("/savehash/<addr>")
def savehash(addr):
	#get the addr from javascript of confirmbtn==>done
	
       	#check the database with filter
	lll = tr_list.query.filter_by(bitcoinaddr=addr)
	print lll
	print lll[0]
	etat = lll[0].etat
	print "etat is ===============================>", etat
	if etat == 1:
		
		return "votre checksum a bien ete enregistre avec le txid " + lll[0].txid
	#add another field to database which contains 0 or txid
	#if etat=1 print thetxid else print still waiting for transaction
	else:
		return "toujours en attente d'envoie de 0.0005 BTC a cette addresse " + addr + " pour pouvoir enregistrer votre checksum"
	#dest_addr="mj9z6Y7B9iwbCHaiskTTw3Wm3Au4mrqNk4"
	
	

	#print "success here is the txid: " + transactionid

@app.route("/recherche")
@login_required
def recherche():
	return render_template("search.html")


@app.route("/find/<txid>")
@login_required
def find(txid):
	#after importing from getdata we pass the txid
	data = finddata(txid)
	print data
	if (data!="tilt"):
		return data[:64] + " enregistree le " +datetime.datetime.fromtimestamp(int(data[64:])).strftime('%Y-%m-%d %H:%M:%S')	
	else:
		return "txid invalide, veuillez verifier avant de ressayer"


	

if __name__ == "__main__":
	app.run('0.0.0.0',5000,debug = True)
