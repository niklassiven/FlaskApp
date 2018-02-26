from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

#My SQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
	try:
		#Read the user input from the UI (webpage)
		_name = request.form['inputName']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']


		#Check if the user input is valid, if not return error message in the console
		if _name and _email and _password:

			#If the input is good, then call mySQL
			conn = mysql.connect()
			cursor =conn.cursor()

			#Creating hashed passwords by using Werkzeug library
			_hashed_password = generate_password_hash(_password)

			#Calling the SQL procedure to create users that was created
			cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
			data = cursor.fetchall()

			#Returns this to the Ajax script
			if len(data) == 0:
				conn.commit()
				return json.dumps({'message': 'User created successfully!'})
			else:
				return json.dumps({'error':str(data[0])})

		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})

	except Exception as e:
		return json.dumps({error:str(e)})
	finally:
		cursor.close()
		conn.close()


if __name__ == "__main__":
	app.run()