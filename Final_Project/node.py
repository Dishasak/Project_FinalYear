from flask import Flask
from flask import Flask, jsonify, request, render_template
from flask_session import Session

import json
import sys

from flask import Flask, flash, redirect, render_template, \
     request, url_for ,session

from datetime import datetime
from transaction import Transaction
##import constant as cnst
import sqlite3 as sql

from tkinter import * 
from tkinter import messagebox 
import tkinter as tk

from Fn_CreateStack import create_stack
from Fn_StackShares import StackShares
node = Flask(__name__)
node.config['SESSION_TYPE'] = 'banker'
node.config['SECRET_KEY'] = 'super'

sess = Session()


@node.route('/')
def  first():
    return  render_template('index.html')

@node.route('/new')
def  new():
    return  render_template('newkyc.html')

@node.route('/menu')
def  menu():
    return  render_template('menu.html')


@node.route('/login', methods=['POST'])
def  login():
    
    error = None
    if  request.method  ==  'POST':
        username=request.form['username']
        password=request.form['password']
        con = sql.connect("vcbank")
        cur = con.cursor()
        ##statement = f"SELECT * from users WHERE username='{username}' AND Password = '{password}';"
        statement = "select * from Users where username='"+username+"' and password='"+password+"'"
        cur.execute(statement)
        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login failed")
            error  =  'Invalid  username  or  password.  Please  try  again  !'
        else:
            return  render_template('bankmenu.html')
            
    return  render_template('index.html',  error  =  error)


@node.route('/div2createacc')
def  div2createacc():
    return  render_template('newaccount.html')


@node.route('/div2updateMob')
def  div2updateMob():
    return  render_template('updatemob.html')

@node.route('/div2kyc')
def  div2kyc():
    return  render_template('kycupdate.html')

@node.route('/div2depo')
def  div2depo():
    return  render_template('deposite.html')

@node.route('/div2with')
def  div2with():
    return  render_template('withdraw.html')

@node.route('/div2bal')
def  div2bal():
    return  render_template('balance.html')

@node.route('/div2close')
def  div2close():
    return  render_template('closeacct.html')

@node.route('/div2bak')
def  div2bak():
    return  render_template('bankmenu.html')

@node.route('/div2mini')
def  div2mini():
    return  render_template('ministatement.html')

@node.route('/div2varify')
def  div2varify():
    return  render_template('kycvarify.html')

@node.route('/closeacct', methods=['POST'])
def  closeacct():
    report = None
    if  request.method  ==  'POST':
        
        accno =request.form['accno']
        adharno = request.form['adharno']
        dob = request.form['dob']
        panid = request.form['panid']
        drivlic = " "  ##request.form['drivlic']

        con = sql.connect("vcbank")
        cur = con.cursor()
        statement = "select * from kyc where accno='"+accno+"'"
        cur.execute(statement)
        data = cur.fetchall()
        print(data)

        if len(data)==0:
            print("No Such record found or already closed")
            report="No Such record found or already closed"
            return  render_template('closeacct.html',  report  =  report)


        dval=[]


        for ele in data:
            print(ele)
            
        print(ele[1])    
        

        if adharno==adharno :
         ###and ele[2]==dob and  (ele[3]==panid)

            statement = "delete from newcustomer where accno='"+accno+"'"
            cur.execute(statement)

            statement = "delete  from kyc where accno='"+accno+"'"
            cur.execute(statement)

            statement = "delete  from banktran where accno='"+accno+"'"
            cur.execute(statement)

            con.commit()

            print('Account Varified and closed')
            report='Account Varified and closed'
            
        else:
            print('Account Not Varified NOT Closed')
            report='Account Not Varified NOT Closed'
        
    return  render_template('closeacct.html',  report  =  report)
    


    

@node.route('/addcustomer', methods=['POST'])
def  addcustomer():

    report = None
    if  request.method  ==  'POST':

        con = sql.connect("vcbank")
        cur = con.cursor()

        statement = "select COUNT(*) from newcustomer"
        cur.execute(statement)

        accno = 15000+cur.fetchone()[0]+1

        print(accno)
        
        fullname=request.form['fullname']
        address=request.form['address']
        dob=request.form['dob']
        emailid=request.form['emailid']
        mobno=request.form['mobno']
        balance=request.form['balance']

        records = [(fullname,accno, address,dob,emailid,mobno,balance)]
        cur.executemany('INSERT INTO newcustomer VALUES(?,?,?,?,?,?,?);',records);

        records = [(datetime.now(), accno, "New Account",0,balance,balance)]
        cur.executemany('INSERT INTO banktran VALUES(?,?,?,?,?,?);',records);

        records = [(accno,"","","","","Not Updated")]
        cur.executemany('INSERT INTO kyc VALUES(?,?,?,?,?,?);',records);

        con.commit()
        report=fullname+" Account No. "+str(accno)+" Created Succefully" 

        ###flash('You were successfully logged in')

        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        messagebox.showinfo("Info", report) 
        root.destroy()

        return  render_template('bankmenu.html',  report  =  report)

        
@node.route('/newkyc', methods=['POST'])
def newkyc():

    report = None
    if  request.method  ==  'POST':

        accno =request.form['accno']
        adharno = request.form['adharno']
        dob = request.form['dob']
        panid = request.form['panid']
        drivlic = ""  ##request.form['drivlic']
        
        con = sql.connect("vcbank")
        cur = con.cursor()

        #fetch dob comapre if Invalid Message

        statement = "select dob from newcustomer where accno='"+accno+"'"
        cur.execute(statement)

        Sdob=cur.fetchone()[0]

        print('Sdob',Sdob)

        if dob!=Sdob:

            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Invalid", "Birth Date not varified") 
            root.destroy()

        else:
            statement = "UPDATE kyc SET adhar='"+adharno+"',dob='"+dob+"',panid='"+panid+"',drvlic='"+drivlic+"',status='Updated'  where accno='"+accno+"'"
            cur.execute(statement)
            con.commit()
            
            startTime = datetime.now()

            ##Create Stack
            drive=get_drive();
            create_stack(accno,drive)


            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", "KYC Updated , customer share stored ") 
            root.destroy()
    return render_template('kycupdate.html', result="KYC Registered") 


@node.route('/accountReport')
def  accountReport():
        statement = "select * from newcustomer,kyc where  newcustomer.accno=kyc.accno"
        con = sql.connect("vcbank")
        cur = con.cursor()
        cur.execute(statement)
        data = cur.fetchall()

        print(data)
        return  render_template('accountlist.html',  data  =  data)
    
@node.route('/ministat', methods=['POST'])
def  ministat():

    if  request.method  ==  'POST':
        accno=request.form['accno']
        
        con = sql.connect("vcbank")
        cur = con.cursor()
        statement = "select * from banktran where accno='"+accno+"'"
        cur.execute(statement)
        data = cur.fetchall()

        print(data)
        return  render_template('ministatement.html',  data  =  data)
    

@node.route('/depoamt', methods=['POST'])
def  depoamt():

    report = None
    if  request.method  ==  'POST':

        accno=request.form['accno']
        amt=request.form['amount']

        con = sql.connect("vcbank")
        cur = con.cursor()

        statement = "select status from kyc where accno='"+accno+"'"
        cur.execute(statement)

        try:
            stat=cur.fetchall()[0]
            print(stat)
        except:
            report="Invalid Account Number"
            print(report)
            return  render_template('deposite.html',  report  =  report)
            
        
        if stat[0]=="Varified":
        
            statement = "select balance from newcustomer where accno='"+accno+"'"
            cur.execute(statement)

            balance=cur.fetchone()[0]+int(amt)

            print(balance)
            
            records = [(datetime.now(), accno, "Amount Deposited",0,amt,balance)]
            cur.executemany('INSERT INTO banktran VALUES(?,?,?,?,?,?);',records);


            statement = "UPDATE newcustomer SET balance ="+str(balance)+" where accno='"+accno+"'"
            cur.execute(statement)
            con.commit()
            report="Amount Deposited"
        else:
            report="KYC no verified Make KYC first"
        
        return  render_template('deposite.html',  report  =  report)

@node.route('/updateacct', methods=['POST'])
def  updateacct():
    
    if  request.method  ==  'POST':

        accno=request.form['accno']
        mobno=request.form['mobno']

        con = sql.connect("vcbank")
        cur = con.cursor()

        statement = "update newcustomer set mobno='"+mobno+"' where accno='"+accno+"'"

        print(statement)
        cur.execute(statement)
        con.commit()
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        messagebox.showinfo("Info", "Mobile Number Updated") 
        root.destroy()
        
        return  render_template('bankmenu.html')
 
@node.route('/withdrawamt', methods=['POST'])
def  withdrawamt():
    report = None
    if  request.method  ==  'POST':

        accno=request.form['accno']
        amt=request.form['amount']

        con = sql.connect("vcbank")
        cur = con.cursor()

        statement = "select status from kyc where accno='"+accno+"'"
        cur.execute(statement)

        try:
            stat=cur.fetchall()[0]
            print(stat)
        except:
            report="Invalid Account Number"
            print(report)
            return  render_template('withdraw.html',  report  =  report)
            
        
        if stat[0]=="Varified":
            statement = "select balance from newcustomer where accno='"+accno+"'"
            cur.execute(statement)

            balance=cur.fetchone()[0]-int(amt)

            if balance>1000:
                print(balance)
                
                records = [(datetime.now(), accno, "Amount Withdraw",amt,0,balance)]
                cur.executemany('INSERT INTO banktran VALUES(?,?,?,?,?,?);',records);

                statement = "UPDATE newcustomer SET balance ="+str(balance)+" where accno='"+accno+"'"
                cur.execute(statement)
                con.commit()
                report="Amount Withdrawn"
            else:
                report="Amount Not Suffucient"
        else:
            report="KYC no verified Make KYC first"
            
        return  render_template('withdraw.html',  report  =  report)
    

@node.route('/checkbalance', methods=['POST'])
def  checkbalance():

    report = "Error"
    if  request.method  ==  'POST':
        
        accno=request.form['accno']
        con = sql.connect("vcbank")
        cur = con.cursor()
        
        statement = "select balance from newcustomer where accno='"+accno+"'"
        cur.execute(statement)
        balance=cur.fetchone()[0]

        print("Balance "+str(balance))
        return  render_template('balance.html',  report  =  balance)        



@node.route('/showkyc', methods=['GET'])
def showkyc():
    return render_template('view.html', result=json_object) 


@node.route('/kycvarify2', methods=['POST'])
def kycvarify2():

    report = None
    if  request.method  ==  'POST':    
        accno =request.form['accno']

        con = sql.connect("vcbank")
        cur = con.cursor()
        
        #statement = "select adhar,dob,panid from kyc where accno='"+accno+"'"
        #cur.execute(statement)

        #data1=cur.fetchone()

        

        res=StackShares(accno)

        print("Result "+ str(res))
        
        if res==1:

            statement = "UPDATE kyc SET status='Varified' where accno='"+accno+"'"
            cur.execute(statement)
            con.commit()
            
            return render_template('./valid.html')
        else:
            return render_template('./invalid.html')


###validation    
##def isValid(chainList):
##    
##    for i in range(len(chainList)-1):
##        previousBlock = chainList[i]
##        currentBlock = chainList[i+1]
##        temp = chainList[i+1]
##        temp.hash = ""
##        temp.nonce = 0
##        temp.mine(cnst.DIFFICULTY)
##
##        if currentBlock.hash != temp.hash:
##            return False
##
##        if currentBlock.index == previousBlock.index:
##            return False
##        
##        if currentBlock.previousHash != previousBlock.hash:
##            return False
##    
##    return True

def get_drive():
    import os
    import win32api
    import win32file
    os.system("cls")
    drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
    for device in drives:
        type = win32file.GetDriveType(device)
        if type==2:
            print("Drive: " ,device)
    return device







if __name__== '__main__':

    if len(sys.argv) >= 2:
        port = sys.argv[1]
    else:
        port = 8000

    node.run(host='127.0.0.1', port=port)
