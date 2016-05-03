import subprocess

def getnewaddress():
	return subprocess.check_output(['bitcoin-cli','-regtest','getnewaddress','""']).decode("utf-8").rstrip("\n")


#a=getnewaddress()
#print a
