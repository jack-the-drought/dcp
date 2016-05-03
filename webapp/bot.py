from database import db,tr_list
import subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib,sys
from flask import Flask, request, render_template
from newsavedata import *
from getaddressbalance import *

#go through database
#if etat = 0
#checkwith getreceivedbyaddress if amount>0.0005
#create+sign+send+validate
invalidhashes = tr_list.query.filter_by(etat=0)

numberofinvalid = invalidhashes.count()

invalidlst = invalidhashes.all()

for i in range(numberofinvalid):
        print i
        xa7 = invalidlst[i]
        adr = xa7.bitcoinaddr
        solde = getsolde(adr)
        print "solde is ", solde
        solde = float(solde)
        if solde >= 0.0005:
		
		print "received money now saving the hash"		
		
		filehash = xa7.filehash
		dest_addr = "mj9z6Y7B9iwbCHaiskTTw3Wm3Au4mrqNk4" #fix address for internal transactions
		data=filehash.decode("hex") # from database
		transactionid=save(data,dest_addr)
		validateblocks()
		xa7.etat = 1
		db.session.commit()		
		xa7.txid = transactionid
		db.session.commit()
