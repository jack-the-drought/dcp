import subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib,sys
from flask import Flask, request, render_template
from newsavedata import *
from getnewaddr import getnewaddress
from database import db
from database import tr_list

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("newspindex.html")

@app.route("/newsavehash/<hashh>")
def savethehash(hashh):
	new_address = getnewaddress()
	new_tr = tr_list(hashh+str(int(time.time())),new_address,0,"blanko")
	db.session.add(new_tr)
	db.session.commit()
	
	return render_template("confirmbtn.html",hash=hashh,addr = new_address)
	


@app.route("/savehash/<addr>")
def savehash(addr):
	#get the addr from javascript of confirmbtn==>done
	
       	#check the database with filter
	lll = tr_list.query.filter_by(bitcoinaddr=addr)
	etat = lll[0].etat
	if etat == 1:
		return "votre checksum a bien ete enregistre avec le txid " + lll[0].txid
	#add another field to database which contains 0 or txid
	#if etat=1 print thetxid else print still waiting for transaction
	else:
		return "toujours en attente d'envoie de 0.0005 BTC a cette addresse " + addr + " pour pouvoir enregistrer votre checksum"
	#dest_addr="mj9z6Y7B9iwbCHaiskTTw3Wm3Au4mrqNk4"
	
	

	#print "success here is the txid: " + transactionid

	
	


	

if __name__ == "__main__":
	app.run('0.0.0.0',5000,debug = True)
