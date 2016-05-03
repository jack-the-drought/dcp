from flask import Flask, request, render_template
from getdata import *
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("search.html")

@app.route("/find/<txid>")
def find(txid):
	#after importing from getdata we pass the txid
	data = finddata(txid)
	print data
	return data

if __name__ == "__main__":
	app.run('0.0.0.0',5000,debug = True)
