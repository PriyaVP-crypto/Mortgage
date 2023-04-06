import os
import json
import requests
import tornado.web
import tornado.ioloop
import tornado.autoreload
import sys
import asyncio
#import psycopg2
import time
#import matplotlib.pyplot as plt

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))
#port=8000
class landingPage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")
        
class HomePage(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html")

class Login(tornado.web.RequestHandler):
    def post(self):
        #base_url = 'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/custReg?acctId='
        # 100000001001 is the only working answer
        #headers = {'Content-Type': 'application/json'}
        print("inside login")
        username = str(self.get_body_argument("uname"))
        print(username)
        pwd = str(self.get_body_argument("pass"))
        print(pwd)
        #end_url= base_url+str(self.get_body_argument("accnt"))
        #req = requests.get(end_url, headers=headers, auth=('701e3938-c7c7-4568-9e3b-d474bfb39700', ''), verify=False)
        #json_out = req.json()
        print("json")
        if username =="admin" and pwd == "adminpass":
            print("success")
            self.render("static/indexx.html")
        else:
            print("no")
            self.render("static/trial.html")
        #print(json_out)
        #self.render("static/genericresp.html",msg=json_out['CSRGRES']['CSRGRES']['MESSAGES'],cname=json_out['CSRGRES']['CSRGRES']['CUSTOMER_NAME'],cid=json_out['CSRGRES']['CSRGRES']['CUSTOMER_ID'],date=json_out['CSRGRES']['CSRGRES']['SYS_DATE'],time=json_out['CSRGRES']['CSRGRES']['SYS_TIME'],bloc="regreq")



class basicRevHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/reversal.html")

class predictScore(tornado.web.RequestHandler):
    def post(self):
        base_url = 'https://192.86.32.113:19443/api_fraud_detection/fraudDetection?'
        #base_url = 'https://gateway.aipc1.cp4i-b2e73aa4eddf9dc566faa4f42ccdd306-0001.us-east.containers.appdomain.cloud/sachinsorg/sandbox/payments/pymntRev?acctId='
        #base_url = 'https://api.eu-gb.apiconnect.appdomain.cloud/m1ganeshtcscom1543928228162-dev/sb/payments/pymntRev?acctId='
        # 100000001001 is the only working answer
        headers = {'Content-Type': 'application/json'}

        mername=str(self.get_body_argument("mername"))
        usr=str(self.get_body_argument("usr"))
        amt=str(self.get_body_argument("amt"))
        merstate=str(self.get_body_argument("merstate"))
        chip=str(self.get_body_argument("chip"))
        err=str(self.get_body_argument("err"))
        mcc=str(self.get_body_argument("mcc"))
        mercity=str(self.get_body_argument("mercity"))
        card=str(self.get_body_argument("card"))

        #end_url= base_url+str(self.get_body_argument(mername"accnt"))+"&transId="+str(self.get_body_argument("trans"))+"&revAmt="+str(self.get_body_argument("debit_amt"))
        end_url= base_url+'merchantxname='+mername+"&user1="+usr+"&amount="+amt+"&merchantxstate="+merstate+"&usexchip="+chip+"&errorsx="+err+"&mcc="+mcc+"&merchantxcity="+mercity+"&card="+card
        req = requests.get(end_url, headers=headers, auth=('ibmuser', 'ibmuser'), verify=False)
        json_out = req.json()
        print("before")
        #print(json_out)
        jsonstruct=json_out
        #print(jsonstruct)
        jsonstruct=json.dumps(jsonstruct)
        json_load=json.loads(jsonstruct)
        #print(json_load["MODELOUT"]["MODELOUP"]["PROBABILITYX1X"])
        print("df")

        val1=json_load['MODELOUT']['MODELOUP']['PROBABILITYX1X']
        val2=json_load['MODELOUT']['MODELOUP']['PROBABILITYX0X']
        #print(val1)
        val1=round(val1,16)
        val2=round(val2,16)
        #print (val1)
        val1=round((val1*100),2)
        val2=round((val2*100),2)
        #print(val1)
        #val1=round(val1,2)
        #print(val1)
        #percent1=val1
        #percent2=int(json_load['MODELOUT']['MODELOUP']['PROBABILITYX0X'])*100
        print(val1,val2)
        labels= ['Risk for transfer', 'Non-risk for transfer']
        colors=['#14213d','#e63946']
        sizes= [val1,val2]
        #plt.pie(sizes,labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
        #plt.axis('equal')
        #plt.show()

        self.render("static/result.html",label=labels,color=colors,size=sizes,
                    x1x=json_load['MODELOUT']['MODELOUP']['PROBABILITYX1X'],
                    xox=json_load['MODELOUT']['MODELOUP']['PROBABILITYX0X'],
                    bloc="predictScore", jsonstruct=jsonstruct,
                    mername=mername,usr=usr,amt=amt,merstate=merstate,
                    chip=chip,err=err,mcc=mcc,mercity=mercity,card=card)
        



if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", landingPage),
        (r"/predictScore", predictScore),

    ])
    print("commit")
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.listen(port)
    # TODO remove in prod
    #print("inside win")
    #server=HTTPServer(app)
    tornado.autoreload.start()
    print("I'm listening on port specified")
    print(port)
    tornado.ioloop.IOLoop.current().start()
