import subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib,sys
from flask import Flask, request, render_template
from newsavedata import *
app = Flask(__name__)

@app.route("/")
def index():
        return render_template("index.html")


@app.route("/savehash/<hashh>")
def savehash(hashh):
        #call func here
        dest_addr="mhP3FTFtmGb8VLybd12JPZVscvJv2SA8C6"
        data=hashh.decode("hex")
        transactionid=save(data,dest_addr)
        validateblocks()
        print "success here is the txid: " + transactionid


        return transactionid
if __name__ == "__main__":
        app.run('0.0.0.0',5000,debug = True)
