from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alice:alicepass@172.17.0.1/hoh'
db = SQLAlchemy(app)

class tr_list(db.Model):
	__tablename__ = 'tr_list'
	
	filehash = db.Column(db.String(80), unique=True,primary_key=True)
	bitcoinaddr = db.Column(db.String(80), unique=True)
	etat = db.Column(db.Integer)
	txid = db.Column(db.String(80))
	def __init__(self,filehash,bitcoinaddr,etat,txid):
		
		self.filehash = filehash
		self.bitcoinaddr = bitcoinaddr
		self.etat = etat
		self.txid = txid
	'''def __repr__(self):
		return '<filehash %r>' % self.filehash
	'''
