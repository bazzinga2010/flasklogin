from flask import Flask,render_template,redirect,url_for,request,flash
from forms import RegisterForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user,current_user,logout_user,UserMixin,login_required,LoginManager

app = Flask(__name__)
app.secret_key="thisisasecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#error
login_manager = LoginManager()#create object of login manager
login_manager.init_app(app)#initialize login manager
#login_manager.login_view = "login"#if not login then send to login page

class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key = True)
	firstname = db.Column(db.String(15))
	lastname = db.Column(db.String(15))
	username = db.Column(db.String(20),unique = True)
	password = db.Column(db.String(20))

@login_manager.user_loader#this is used to
def load_user(user_id):# create the object of 
	return User.query.get(int(user_id) )# particular user id.

@app.route("/index")
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/login",methods=['GET','POST'])
def login():
	form = LoginForm()
	error = None
	if request.method == 'POST':
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user,remember=form.remember.data)
				return redirect(url_for("home"))
		else:
			error = "invalid credentials!"
			return render_template("login.html",error=error,form=form)

	return render_template("login.html",form=form,title='Login Page')

@app.route("/register",methods = ['POST','GET'])
def register():
	form = RegisterForm()
	error = None
	if request.method == 'POST':
		if form.validate_on_submit():
			newuser = User(firstname=form.firstname.data,lastname=form.lastname.data,username=form.username.data,password=form.password.data)
			db.session.add(newuser)
			db.session.commit()
			flash("You are successfully registered")
			return redirect(url_for('login'))
	return render_template("register.html",form = form,title='Register Page')

@app.route("/home")
#@login_required#if login the only access to this page
def home():
	form=LoginForm()
	if current_user.is_authenticated==False:
		loginwarning = "you have to first login to access this page"
		return render_template("login.html",loginwarning=loginwarning,form=form)
	else:
		return render_template("home.html",name=current_user.username)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect('index')

@app.route("/about")
def about():
	return render_template("about.html",title="about-page")




if __name__ == '__main__':
	app.run(debug = True)