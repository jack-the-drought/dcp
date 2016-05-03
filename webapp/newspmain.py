import subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib,sys
from flask import Flask, request, render_template
from newsavedata import *
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("newspindex.html")

@app.route("/newsavehash/<hashh>")
def savethehash(hashh):
	return render_template("confirmbtn.html",hash=hashh)
	


@app.route("/savehash/<hashh>")
def savehash(hashh):
	#call func here
	dest_addr="mj9z6Y7B9iwbCHaiskTTw3Wm3Au4mrqNk4"
	data=hashh.decode("hex")
	transactionid=save(data,dest_addr)
	validateblocks()
	print "success here is the txid: " + transactionid

	
	return transactionid


	

if __name__ == "__main__":
	app.run('0.0.0.0',5000,debug = True)
