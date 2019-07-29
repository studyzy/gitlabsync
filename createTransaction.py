# -*- coding=utf-8 -*-
import requests
import json
import re
import unittest
from time import sleep
import time

class createTrans(unittest.TestCase):


    def setUp(self):
        self.domain = 'http://localhost:8545/'
        self.headers = {'Content-Type':'application/json'}
        self.genesisAddress = "P1CNy7143nnbuohMjR31m4UaMnU6b6X7tqB"
        self.copygenesisAddress = "P1FC2WC7hscSEgqSMMbxTDZwkMTzjWniUXf" #A
        self.recieverAddr1 = "P1Mx7VmpvPS3a77bzjEvmA7oMg78pmj1X31" #B
        self.recieverAddr2 = "P1GxQKxo7L6paJ53ekEm57bcUk9zES3UfTo" #C

    def tearDown(self):
        pass

    def convertToCopyAddr(self):
        createResult,addr= self.cmdCreateTransaction(self.genesisAddress,self.copygenesisAddress,990000000,100)
        signResult = self.signRawTransaction(createResult)
        self.sendRawTransaction(signResult)

    def testGen(self):

        for i in range(100):
            result, recievAddr1 = self.cmdCreateTransaction(self.copygenesisAddress, self.recieverAddr1, 101, 10890)
            re_decode = self.ptn_decode(result)
            if i==0:
                re_combine = self.combine(outputResult=re_decode, recieverAddr=recievAddr1, n=99)
            else:
                re_combine = self.combine(outputResult=re_decode, recieverAddr=recievAddr1, n=99,txid=re_sendTrans)
            re_encode = self.ptn_encode(re_combine)
            re_signTrans = self.signRawTransaction(re_encode)
            re_sendTrans = self.sendRawTransaction(re_signTrans)
            print re_sendTrans
            re_batchSign=self.batchSign(re_sendTrans,self.recieverAddr1,self.recieverAddr2,1,100)
            self.BtoC(re_batchSign)


    #def generateSender(self,result,recievAddr1,txid):
    def generateSender(self,**arg):

        pass
        #return re_sendTrans

    def getAddrUtxos(self,address,type):
        data = {
            "jsonrpc": "2.0",
            "method": "ptn_getAddrUtxos",
            "params": [address],
            "id": 1
        }
        data = json.dumps(data)
        response = requests.post(url=self.domain, data=data, headers=self.headers)
        result1 = json.loads(response.content)
        #print 'Current Utxos : ' + result1['result'] + '\n'
        txid = re.findall(r"\"txid\":\"(.+?)\",\"message_index\"", result1['result'])
        #print txid[0]
        amount = re.findall(r"\"amount\":(.+?)\,\"asset\"", result1['result'])
        #print int(amount[0])
        #用于旧版创建交易
        if type == 0:
            return txid[0],int(amount[0])
        else:
            #print "Return amount:" + amount[0]
            return amount[0]

    def cmdCreateTransaction(self,senderAddr,recieverAddr,senderAmount,poundage):
        data = {
            "jsonrpc":"2.0",
            "method":"ptn_cmdCreateTransaction",
            "params":
                [senderAddr,recieverAddr,senderAmount,poundage],
            "id":1
        }
        data = json.dumps(data)
        response = requests.post(url=self.domain, data=data, headers=self.headers)
        result1 = json.loads(response.content)
        print 'CreateTrans Result: ' + result1['result'] + '\n'
        return result1['result'],recieverAddr

    def ptn_decode(self,result):
        data = {
                "jsonrpc":"2.0",
                "method":"ptn_decodeTx",
                "params":[
                    result
	            ],
	            "id":1
        }
        data = json.dumps(data)
        #print "decode post body: " + data
        response = requests.post(url=self.domain, data=data, headers=self.headers)
        result1= json.loads(response.content)
        outputResult = result1['result']
        print 'Decode Result: ' + outputResult + '\n'
        return outputResult

    #def combine(self,outputResult,recieverAddr,n,txid):
    def combine(self,**arg1):
        if arg1['n'] != 0:
            outputTemp = arg1['outputResult'].split("OP_CHECKSIG\"},")
            if len(arg1) == 4:
                outputTemp[0] = re.sub(r'\"txid\":\"(.+?)\",\"message_index\"',r'\"txid\":\"' + arg1['txid'] + '\\",\\"message_index\\"', outputTemp[0])
            outputTemp1 = re.findall(r'{\"amount\"(.+?)' + arg1['recieverAddr'] + '(.+?)OP_EQUALVERIFY', outputTemp[0])
            if outputTemp1:
               outputPart1 = '{\"amount\"' + outputTemp1[0][0] + arg1['recieverAddr'] + outputTemp1[0][1] + 'OP_EQUALVERIFY OP_CHECKSIG\"},'
                # print outputPart1
            else:
                outputTemp1 = re.findall(r'{\"amount\"(.+?)' + arg1['recieverAddr'] + '(.+?)OP_CHECKSIG', outputTemp[1])
                outputPart1 = '{\"amount\"' + outputTemp1[0][0] + arg1['recieverAddr'] + outputTemp1[0][1] + 'OP_CHECKSIG\"},'
                # print outputPart1
            outputPart = ""
            for i in range(arg1['n']):
                outputPart = outputPart + outputPart1
                conbineResult = re.sub(r'OP_EQUALVERIFY OP_CHECKSIG\"}(.+?){\"amount\"','OP_EQUALVERIFY OP_CHECKSIG\"},' + outputPart + '{\"amount\"',arg1['outputResult'], 1)
            return conbineResult
        else:
            return arg1['outputResult']


            #if txid!=0:
            ''''
            if n != 0:
                outputTemp = outputResult.split("OP_CHECKSIG\"},")
                outputTemp[0] = re.sub(r'\"txid\":\"(.+?)\",\"message_index\"',r'\"txid\":\"' + txid + '\\",\\"message_index\\"', outputTemp[0])
                outputTemp1 = re.findall(r'{\"amount\"(.+?)' + recieverAddr + '(.+?)OP_EQUALVERIFY', outputTemp[0])
                if outputTemp1:
                    outputPart1 = '{\"amount\"' + outputTemp1[0][0] + recieverAddr + outputTemp1[0][1] + 'OP_EQUALVERIFY OP_CHECKSIG\"},'
                    #print outputPart1
                else:
                    outputTemp1 = re.findall(r'{\"amount\"(.+?)' + recieverAddr + '(.+?)OP_CHECKSIG', outputTemp[1])
                    outputPart1 = '{\"amount\"' + outputTemp1[0][0] + recieverAddr + outputTemp1[0][1] + 'OP_CHECKSIG\"},'
                    #print outputPart1
                outputPart = ""
                for i in range(n):
                    outputPart = outputPart + outputPart1
                    conbineResult = re.sub(r'OP_EQUALVERIFY OP_CHECKSIG\"}(.+?){\"amount\"','OP_EQUALVERIFY OP_CHECKSIG\"},' + outputPart + '{\"amount\"', outputResult, 1)
                return conbineResult
            else:
                return outputResult
            '''

        # YOU MUSTN'T REMOVE CODE BELOW!!!
        # conbineResult = re.sub(r"(\")", '\\"', conbineResult)
        # conbineResult = re.sub(r"(\:\"\")", ':', conbineResult)
        # conbineResult = "\"" + conbineResult + "\""
        # print conbineResult

    def ptn_encode(self, result):
            data = {
                "jsonrpc": "2.0",
                "method": "ptn_encodeTx",
                "params": [
                    result
                ],
                "id": 1
            }
            data=json.dumps(data)
            response = requests.post(url=self.domain, data=data, headers=self.headers)
            #print "encode Result:"+ response.content
            result1 = json.loads(response.content)
            print "Encode Result: " + str(result1['result'])
            return result1['result']

    def signRawTransaction(self,result):
        data ={
                "jsonrpc":"2.0",
                "method":"ptn_signRawTransaction",
                "params":
                [
                result,
                'ALL',
                "1"],
	            "id":1
            }

        data = json.dumps(data)
        response = requests.post(url=self.domain, data=data, headers=self.headers)
        result1 = json.loads(response.content)
        print response.content
        print 'SignTrans Result: '+ str(result1['result']['hex']) + '\n'
        return str(result1['result']['hex'])

    def batchSign(self,result,senderB,receiverC,amount,times):
        data = {
            "jsonrpc": "2.0",
            "method": "ptn_batchSign",
            "params":
                [result,
                 senderB,
                 receiverC,
                 amount,
                 times,
                 "1"],
            "id": 1
        }
        data = json.dumps(data)
        response = requests.post(url=self.domain, data=data, headers=self.headers)
        result1 = json.loads(response.content)
        print str(result1['result'])
        #print 'batchSign Result: ' + str(result1['result']) + '\n'
        return result1['result']

    def sendRawTransaction(self,result):
        data = {
                "jsonrpc":"2.0",
                "method":"ptn_sendRawTransaction",
                "params":
                [
                    result],
            "id":1
        }
        data = json.dumps(data)
        response = requests.post(url=self.domain, data=data, headers=self.headers)
        result1 = json.loads(response.content)
        print 'SendTrans Result: '+ str(result1) + '\n'
        return result1['result']




    def combineBtoC(self,txid):
        print str(time.strftime("%Y-%m-%d %X")) + "  Begin\n"
        signResult = open(r'geneSignResult.txt', 'a+', buffering=1)
        for i in range(100):
            template = '{\"tx_hash\":\"0x07d4dc0a711469a28c7ed94d962080715dcd00083fef1cf9c2059df87f0bf517\",\"payment\":{\"inputs\":[{\"txid\":\"' + txid + '\",\"message_index\":0,\"out_index\":'+str(i)+',\"unlock_script\":\"cc95e91d7255a3a6d58cdde47e5019a098099f610f2b346851bf9a1503288d0f41356e457c4453adbbf6280f094200c502b3bddabf07873631b0db70be53c658 022082000fda53b321e9227e0fb79d4d1615318bd127fdbaa53682bdbafb48437e\"}],\"outputs\":[{\"amount\":400000000,\"asset\":\"PTN+0000000000000\",\"to_address\":\"'+ self.recieverAddr1+'\",\"lock_script\":\"OP_DUP OP_HASH160 6f7a0a5580f0de9ee71ceeff9b01267ff8047f10 OP_EQUALVERIFY OP_CHECKSIG\"},{\"amount\":500000000,\"asset\":\"PTN+0000000000000\",\"to_address\":\"'+ self.recieverAddr2+'\",\"lock_script\":\"OP_DUP OP_HASH160 92143776ab3987efb5e25a6ad2462763187ea322 OP_EQUALVERIFY OP_CHECKSIG\"}],\"locktime\":0},\"vote\":null,\"invoke_request\":null}'
            print "combined template:" + template +"\n"
            re_encode2 = self.ptn_encode(template)
            print 'Encode B2C tx:'+re_encode2
            re_signTrans2 = self.signRawTransaction(re_encode2)
            signResult.flush()
            signResult.write("".join(re_signTrans2) + "\n")
        signResult.close()
        print str(time.strftime("%Y-%m-%d %X")) +"  Finished!\n"


    def BtoC(self,re_batchSign):
        print str(time.strftime("%Y-%m-%d %X")) + "  Begin\n"
        #@signResult = open(r'geneBatchResult.txt', 'a+', buffering=1)
        signResult = open(r'./geneSignResult.txt', 'a+', buffering=1)
        for batchSign in re_batchSign:
            signResult.write("".join(batchSign) + "\n")
            signResult.flush()
        signResult.close()
        print str(time.strftime("%Y-%m-%d %X")) + "  Finished!\n"

if __name__ == '__main__':
    unittest.main()