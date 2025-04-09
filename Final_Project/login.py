from flask import Flask, flash, redirect, render_template, \
     request, url_for
from flask_cors import CORS 

app = Flask(__name__)

@app.route('/')
def  first():
    return  render_template('index.html')

@app.route('/login', methods=['POST'])
def  login():
    error = None
    if  request.method  ==  'POST':
        if request.form['username']  !=  'admin'  or  \
           request.form['password']  !=  'admin':
           error  =  'Invalid  username  or  password.  Please  try  again  !'
        else:
            return  render_template('home.html')

    return  render_template('index.html',  error  =  error)

if __name__ == '__main__':
    app.run(debug=True)


    
