from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://alice:alicepass@172.17.0.1/finaldatabase'
db = SQLAlchemy(app)

class tr_list(db.Model):
	__tablename__ = 'tr_list'
	
	filehash = db.Column(db.String(80), unique=True,primary_key=True)
	bitcoinaddr = db.Column(db.String(80), unique=True)
	etat = db.Column(db.Integer)
	txid = db.Column(db.String(80))
	owner_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	#after database test modify this to insert owner_id along with the transaction
	#Foreign key associated with column 'tr_list.owner_id' could not find table 'User' with which to generate a foreign key to target column 'id'
	def __init__(self,filehash,bitcoinaddr,etat,txid,owner_id=None):
		
		self.filehash = filehash
		self.bitcoinaddr = bitcoinaddr
		self.etat = etat		
		self.txid = txid
		self.owner_id = owner_id
	'''def __repr__(self):
		return '<filehash %r>' % self.filehash
	'''
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, unique=True,primary_key=True)
	name = db.Column(db.String(64), unique=True, nullable = False)
	email = db.Column(db.String(64),unique=True, nullable = False)
	password = db.Column(db.String(64), nullable = False)
	ownedtransactions = db.relationship('tr_list',backref='owner',lazy='dynamic')
	def __init__(self,name,email,password):
		
		self.name = name
		self.email = email
		self.password = hashlib.md5(password).digest().encode("hex")

	def is_authenticated(self):
		return True

	def is_active(self):
		return True
	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode((self.id))

	

    	def __repr__(self):
        	return '<User %r>' %(self.name)
