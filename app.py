from flask import Flask, render_template, request, redirect, url_for, flash, session, logging
from wtforms import Form, BooleanField, StringField, TextAreaField, PasswordField, validators, SelectField
from wtforms.validators import InputRequired, Email, Length
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
#from flask_admin import Admin


app = Flask(__name__)
#Bootstrap(app)

app.secret_key ="Whatdoyouthink"
#configure mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tenant_management_system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initializing mysql
mysql = MySQL(app)

#home page 
@app.route('/')
def index():
	return render_template ("home.html")

#user sign up 
class SignupForm(Form):
	account = SelectField('Account Type:', choices =[('T','Tenant'), ('RM', 'Rental Manager')])
	first_name = StringField('First Name:',[validators.Length(min=1, max= 50),
		validators.DataRequired()])
	last_name = StringField('Last Name:',[validators.Length(min=1, max= 50),
		validators.DataRequired()])
	email = StringField('Email:',[validators.Email(), validators.DataRequired()])
	phone_number = StringField('Phone Number:', [validators.Length(min=5, max= 15),]) 
	password = PasswordField('Password:',[
		validators.DataRequired(),
		validators.EqualTo('confirm',message ='Passwords do not match')
		])
	confirm = PasswordField('Confirm Password:')

@app.route('/signup', methods=['GET','POST'])
def signUp():
	form = SignupForm(request.form)
	if request.method == 'POST' and form.validate():
		account = form.account.data
		first_name = form.first_name.data 
		last_name = form.last_name.data
		email = form.email.data
		phone_number = form.phone_number.data
		password = sha256_crypt.encrypt(str(form.password.data))


		
		#create cursor
		cur = mysql.connection.cursor()

		# Execute query
		cur.execute("INSERT INTO users ( account, first_name, last_name, email, phone_number, password)VALUES (%s, %s, %s, %s, %s, %s)",(
			account, first_name, last_name, email, phone_number, password))
	

		#commit to the database
		mysql.connection.commit()

		#close connection
		cur.close()

		flash("Sign up was successful!", "success")
		return redirect(url_for('login'))
	return render_template('register.html', form=form)



class loginForm(Form):
	email = StringField('Email')
	password = PasswordField('Password')

#user login 
@app.route('/login', methods=['GET','POST'])
def login():
	if session.get('logged_in'):
		flash("You are already logged in",'warning')
		return redirect(url_for('index'))
	form = loginForm(request.form)
	if session.get('logged_in'):
		redirect(url_for('index'))
	if request.method == 'POST' and form.validate():
		#email = request.form['email']
		#password_candidate = request.form['password']
		email = form.email.data 
		password_candidate = form.password.data

		#create cursor 
		cur = mysql.connection.cursor()

		#get user by email 
		result = cur.execute("SELECT * FROM users WHERE email = %s", [email])

		if result > 0:

			#get first one with required credentials 
			data = cur.fetchone()
			password = data ['password']

		#compare passwords 
		if sha256_crypt.verify(password_candidate, password):
				#passed
				session['logged_in']= True
				name = cur.execute("SELECT first_name FROM users WHERE email = %s", [email])
				name = cur.fetchall()
				session['name']= name[0]['first_name']
				account_type = cur.execute("SELECT account FROM users WHERE email = %s", [email])
				if account_type > 0:
					data = cur.fetchall()
					account = data[0]['account']
					if account == "RM":
						session["RM"] = session['name']
						flash('Welcome to your Tenant Manager account','success')
						return redirect(url_for('RentalManager'))

					elif account == "T":
						session["T"] = session['name']
						flash('Welcome to your tenant account','success')
						return redirect(url_for('Tenant'))
					else:
						session["Admin"] = session['name']
						flash('Welcome to your Admin portal','success')
						return redirect(url_for('Admin'))
		

		else: 
			error = 'INVALID LOGIN CREDENTIALS'
			return render_template('login.html', error=error, form=form)
 				#app.logger.info("PASSWORD NOT MATCHED!")
			#close connection 
			cur.close()   

	#else: 
		#error = 'USER NOT FOUND!'
		#return render_template('login.html')

	return render_template ('login.html', form=form)

#logout 
@app.route('/logout')
def logout ():
	session.clear()
	flash('You are now logged out','danger')
	return redirect(url_for('login'))

# Rental Manager dashboard
@app.route('/rentalmanager')
def RentalManager():
	if session.get('RM'):
		return render_template('RMdashboard.html')
	flash("You are not logged in as a RentalManager",'danger')
	return redirect(url_for('login'))

#Tenant manager dashboard 
@app.route('/tenant')
def Tenant():
	if session.get('T'):
		return render_template('Tdashboard.html')
	flash("You should logged in as a Tenant to access this dashboard",'danger')
	return redirect(url_for('login'))

#Admin dashboard 
@app.route('/admin')
def Admin():
	if session.get('Admin'):
		return render_template('admindashboard.html')
	flash("You are not logged in as a site Administrator", 'danger')
	return redirect(url_for('login'))

	
if __name__=="__main__":
	app.run(debug=True)