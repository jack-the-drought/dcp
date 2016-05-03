import subprocess

def getsolde(addr):
	return subprocess.check_output(["bitcoin-cli","-regtest","getreceivedbyaddress",addr]).decode("utf-8").rstrip("\n")
