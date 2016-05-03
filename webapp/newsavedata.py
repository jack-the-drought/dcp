import subprocess,json,time,random,os.path,binascii,struct,string,re,hashlib,sys
def finddata(txid):
	Bitcoin_Client = "bitcoin-cli"
	Testmode = "-regtest"
	location=[Bitcoin_Client]
	location.append(Testmode)
	location.append("getrawtransaction")
	location.append(str(txid))
	rawtransaction=subprocess.check_output(location).decode("utf-8").rstrip("\n")
	print rawtransaction




def save(data,addr):
 
	testnet=True
	try:
		basestring
	except NameError:
		basestring=str
	send_address=addr 
	send_amount=0.00000001
	metadata=data
	Bitcoin_Client = "bitcoin-cli"
	Testmode = "-regtest"
	opreturncharlimit=40 
	minimumfees=0.0001 
	poussiere=0.00001 

	metadata_len=len(metadata)
	if metadata_len>opreturncharlimit:
		exit('still too much')

	output_amount=send_amount+minimumfees 
	inputs_spend=selectinputs1(output_amount, testnet) 
	if 'error' in inputs_spend:
		exit('popop')
	change_amount=inputs_spend['total']-output_amount


	change_address=bitcoin_command('getrawchangeaddress', testnet) 
	outputs={send_address: send_amount} 
	if change_amount>=poussiere:
		outputs[change_address]=change_amount

	raw_txn=create_raw_tranction(inputs_spend['inputs'], outputs, metadata, len(outputs), testnet) 
	print raw_txn
	sign=[Bitcoin_Client]
	sign.append(Testmode)
	sign.append("signrawtransaction")
	sign.append(raw_txn)
	signed = subprocess.check_output(sign).decode("utf-8").rstrip("\n")
	signed = json.loads(signed)
	print signed
	print signed['hex']
	print signed['complete']
	print type(signed)
	sendtransaction=[Bitcoin_Client]
	sendtransaction.append(Testmode)
	sendtransaction.append("sendrawtransaction")
	if signed['complete']==True:
		print "sending.."
		sendtransaction.append(signed['hex'])
		txid = subprocess.check_output(sendtransaction).decode("utf-8").rstrip("\n")
		print "txid==> ",txid
		return txid

def create_raw_tranction(inputs, outputs, metadata, metadata_pos, testnet):
        raw_txn=bitcoin_command('createrawtransaction', testnet, inputs, outputs)
        
        txn_unpacked=unpack_bin1(hextobin1(raw_txn))
 
        metadata_len=len(metadata)
 
        if metadata_len<=75:
                payload=bytearray((metadata_len,))+metadata 
        elif metadata_len<=256:
                payload="\x4c"+bytearray((metadata_len,))+metadata 
        else:
                payload="\x4d"+bytearray((metadata_len%256,))+bytearray((int(metadata_len/256),))+metadata 

 
        metadata_pos=min(max(0, metadata_pos), len(txn_unpacked['vout'])) 
        txn_unpacked['vout'][metadata_pos:metadata_pos]=[{
                'value': 0,
                'scriptPubKey': '6a'+bintohex2(payload) 
        }]
 
        return bintohex2(pack_raw_transaction(txn_unpacked)) 
def bitcoin_command(command, testnet, *args): 
        if True:
                sub_args=["bitcoin-cli"] 
                if testnet:
                        sub_args.append('-regtest')
 
                sub_args.append(command)
 
                for arg in args:
                        sub_args.append(json.dumps(arg) if isinstance(arg, (dict, list, tuple)) else str(arg)) 
 
                raw_result=subprocess.check_output(sub_args).decode("utf-8").rstrip("\n") 
 
                try: 
                        result=json.loads(raw_result) 
                except ValueError:
                        result=raw_result
 
        return result 
def selectinputs1(total_amount, testnet):
        
        unspent_inputs=bitcoin_command('listunspent', testnet, 0)
        if not isinstance(unspent_inputs, list):
                return {'error': 'Could not retrieve list of unspent inputs'}
 
        unspent_inputs.sort(key=lambda unspent_input: unspent_input['amount']*unspent_input['confirmations'], reverse=True)
 
        
        inputs_spend=[]
        input_amount=0
 
        for unspent_input in unspent_inputs:
                inputs_spend.append(unspent_input)
                input_amount+=unspent_input['amount']
                if input_amount>=total_amount:
                        break 
 
        if input_amount<total_amount:
                return {'error': 'Not enough funds are available to cover the amount and fee'}
 
        
        return {
                'inputs': inputs_spend,
                'total': input_amount,
        }
def unpack_bin1(binary): 
        return unpack_bin_buff2(buffered(binary)) 
def unpack_bin_buff2(buffer):
        
 
        txn={
                'vin': [],
                'vout': [],
        }
 
        txn['version']=buffer.shift_unpack(4, '<L') 
 
        inputs=buffer.shift_varint()
        if inputs>100000: 
                return None
 
        for _ in range(inputs):
                input={}
 
                input['txid']=bintohex2(buffer.shift(32)[::-1])
                input['vout']=buffer.shift_unpack(4, '<L')
                length=buffer.shift_varint()
                input['scriptSig']=bintohex2(buffer.shift(length))
                input['sequence']=buffer.shift_unpack(4, '<L')
 
                txn['vin'].append(input)
 
        outputs=buffer.shift_varint()
        if outputs>100000: 
                return None
 
        for _ in range(outputs):
                output={}
 
                output['value']=float(buffer.shift_uint64())/100000000
                length=buffer.shift_varint()
                output['scriptPubKey']=bintohex2(buffer.shift(length))
 
                txn['vout'].append(output)
 
        txn['locktime']=buffer.shift_unpack(4, '<L')
 
        return txn
 
def bintohex2(string):
        return binascii.b2a_hex(string).decode('utf-8')
 
def hextobin1(hex):
        try:
                raw=binascii.a2b_hex(hex)
        except Exception:
                return None
 
 
        return raw 
class buffered():
 
 
        def __init__(self, data, ptr=0):
                self.data=data
                self.len=len(data)
                self.ptr=ptr
         
        def shift(self, chars):
                prefix=self.data[self.ptr:self.ptr+chars]
                self.ptr+=chars
                return prefix
         
        def shift_unpack(self, chars, format):
                unpack=struct.unpack(format, self.shift(chars))
                return unpack[0]
        def shift_varint(self):
                value=self.shift_unpack(1, 'B')
                if value==0xFF:
                        value=self.shift_uint64()
                elif value==0xFE:
                        value=self.shift_unpack(4, '<L')
                elif value==0xFD:
                        value=self.shift_unpack(2, '<H')
 
                return value
        def shift_uint64(self):
                return self.shift_unpack(4, '<L')+4294967296*self.shift_unpack(4, '<L')
 
        def used(self):
                return min(self.ptr, self.len)
        def remaining(self):
                return max(self.len-self.ptr, 0)
 
def pack_raw_transaction(txn):
        binary=b'' 
 
        binary+=struct.pack('<L', txn['version'])
 
        binary+=packvarint1(len(txn['vin']))
 
        for input in txn['vin']:
                binary+=hextobin1(input['txid'])[::-1]
                binary+=struct.pack('<L', input['vout'])
                binary+=packvarint1(int(len(input['scriptSig'])/2)) 
                binary+=hextobin1(input['scriptSig'])
                binary+=struct.pack('<L', input['sequence'])
 
        binary+=packvarint1(len(txn['vout']))
 
        for output in txn['vout']:
                binary+=packint2(int(round(output['value']*100000000)))
                binary+=packvarint1(int(len(output['scriptPubKey'])/2)) 
                binary+=hextobin1(output['scriptPubKey'])
 
        binary+=struct.pack('<L', txn['locktime'])
 
        return binary
 
def packvarint1(integer): 
        if integer>0xFFFFFFFF:
                packed="\xFF"+packint2(integer)
        elif integer>0xFFFF:
                packed="\xFE"+struct.pack('<L', integer)
        elif integer>0xFC:
                packed="\xFD".struct.pack('<H', integer)
        else:
                packed=struct.pack('B', integer)
 
        return packed
 
def packint2(integer):
        upper=int(integer/4294967296) 
        lower=integer-upper*4294967296
 
        return struct.pack('<L', lower)+struct.pack('<L', upper)
def validateblocks():
	subprocess.check_output(["bitcoin-cli","-regtest","generate","1"])
#data = "a"*64 #mysha256sum
'''
try:
	addr=sys.argv[2]
except:
	print sys.argv
	exit("u need to give me the address")	
try:
	data=sys.argv[1]
except:
	data="a"*64
data=data.decode("hex")
transactionid = save(data,addr)
validateblocks()
finddata(transactionid)
'''
#print transactionid
