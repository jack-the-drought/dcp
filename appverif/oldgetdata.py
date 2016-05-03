import sys,subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib
def finddata(txid):
	Bitcoin_Client = "bitcoin-cli"
	Testmode = "-regtest"
	location=[Bitcoin_Client]
	location.append(Testmode)
	location.append("getrawtransaction")
	location.append(str(txid))
	rawtransaction=subprocess.check_output(location).decode("utf-8").rstrip("\n")
	return rawtransaction

try:
	rawtr = finddata(sys.argv[1])
except:
	print "not enough args"
	exit()
Bitcoin_Client = "bitcoin-cli"
TestMode = "-regtest"
decode = [Bitcoin_Client]
decode.append(TestMode)
decode.append("decoderawtransaction")
decode.append(rawtr)
fulltransaction = subprocess.check_output(decode).decode("utf-8").rstrip("\n")
biglist = json.loads(fulltransaction)
#for i in biglist:
#	print i
#	print "***=====================***"
#	print biglist[i]
#	print "*******"
list=biglist["vout"]
#print list
#print "starting now"
#for i in range(len(list)):
#	print i	
#	print "**========**"	
#	print list[i]		
#	print "*********"
slist=list[2]
#print slist
ff = slist['scriptPubKey']['asm']
data = ff.split(" ")[1]
print data
