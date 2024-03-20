from flask import Flask, request, jsonify, render_template, url_for, redirect, send_file
from markupsafe import escape
from pymongo import MongoClient
import os
from os.path import join, dirname
from dotenv import load_dotenv 
from cryptography.fernet import Fernet

#Security Libraries
from flask_talisman import Talisman
from flask_cors import CORS

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = MongoClient(os.environ.get('DB_URL'))
#client = MongoClient('mongodb://localhost:27017/')
db = client.flask_db
users = db.users

#

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

crypt = Fernet(os.environ.get('CRYPT_PASS').encode())

#

app = Flask(__name__)
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': [
            '\'self\'',
            'https://cdnjs.cloudflare.com'
        ]
    }
)
CORS(app)

@app.route("/static/<dirname>/<filename>")
def GettingStaticFiles(dirname, filename):
	return send_file(f"{os.getcwd()}/templates/static/{dirname}/{filename}", as_attachment=True)

@app.route("/static/js/chunks/helpers.segment.js")
def GettingChunkFiles():
	return send_file(f"{os.getcwd()}/templates/static/js/chunks/helpers.segment.js", as_attachment=True)

@app.route("/static/js/kurkle/color")
def GettingKurkleFiles():
	return send_file(f"{os.getcwd()}/templates/static/js/@kurkle/color/color.min.js", as_attachment=True)

@app.route("/")
def Index():
	return render_template('index.html')

@app.route("/files/<file>")
def SendFile(file):
	print(f"{os.getcwd()}/templates/files/{file}")
	return send_file(f"{os.getcwd()}/templates/files/{file}", as_attachment=True)

@app.route("/verify/<username>/<password>")
def VerifyUser(username, password):
	result = {"isUser": False, "role": "", "username": "", "password": ""}
	current_users = list(users.find({}))
	decoded_usernames = []
	decoded_passwords = []
	for c in current_users:
		decoded_usernames.append(crypt.decrypt(c['username'].encode()).decode())
		decoded_passwords.append(crypt.decrypt(c['password'].encode()).decode())
	for u in range(0, len(decoded_usernames)):
		if decoded_usernames[u] == username and decoded_passwords[u] == password:
			result['isUser'] = True
			result['role'] = current_users[u]['role']
			result['username'] = current_users[u]['username']
			result['password'] = current_users[u]['password']
			break
	return result

@app.route('/dashboard')
def SendDashboard():
	username = request.args.get('username')
	password = request.args.get('password')
	current_user = list(users.find({'username': username}))
	if(len(current_user) != 1): 
		return redirect('/')
	elif current_user[0]['username'] == username and current_user[0]['password'] == password:
		return render_template('dashboard.html')	
	else:
		return redirect('/')

@app.route('/GetUserInfo/<username>/<password>')
def GetUserInfo(username, password):
	result = {"isUser": False, "role": "", "username": "", "password": ""}
	current_user = list(users.find({'username': username}))
	if(len(current_user) != 1): 
		return result
	elif current_user[0]['username'] == username and current_user[0]['password'] == password:
		decoded_username = crypt.decrypt(username.encode()).decode()
		decoded_password = crypt.decrypt(password.encode()).decode()
		result = {"isUser": True, "role": current_user[0]['role'], "username": decoded_username, "password": decoded_password}
		return result
	else:
		return result

app.run(debug=True)
	