from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

#engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='n151248@rguktn.ac.in'
app.config['MAIL_PASSWORD']='7036006307'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.secret_key="abc"

mail=Mail(app)
otp=randint(000000,999999)

@app.route("/sample")
def demo():
	 return"hello world welcome to rgukt"

@app.route("/demo")
def d():
	 return"<h1>hello world this is akshay</h1>"

@app.route("/info/details")
def details():
	 return"<h1>hello details</h1>"
@app.route("/details/<name>/<int:salary>/<int:age>")
def info(name,salary,age):
	 return"hello {} salary {} and age {}".format(name,salary,age)

@app.route("/admin")
def admin():
	 return"hello Admin"
@app.route("/student")
def student():
	 return"hello student"
@app.route("/staff")
def staff():
	 return"hello staff"
@app.route("/info/<name>")
def admin_info(name):
	#return"hello admin_info"
	if name=='staff':
		return redirect(url_for('staff'))
	elif name=='admin':
		return redirect(url_for('admin'))
	elif name=='student':
		return redirect(url_for('student'))
	elif name=='admin_info':
		return redirect(url_for('student'))
	else:
		return "No URL"
@app.route("/data")
def demo_html():
	return render_template('sample.html')
#@app.route("/template/<name>/<int:age>/<float:salary>")
#def info1(name,age,salary):
	#return render_template('table.html')
@app.route("/table")
def table():
	sno=28
	name='akshay'
	branch='cse'
	dept='engg'
	return render_template('table.html',s_no=sno,n=name,b=branch,d=dept)

dolly=[{'sno':23,'name':'rakesh','branch':'ece','dept':'coder'},
{'sno':21,'name':'pri','branch':'chem','dept':'designer'}]
@app.route("/dummy_data")
def dummy1():
	return render_template('dummy.html',dummy_data=dolly)

@app.route("/cal/<int:number>")
def fraction(number):
	return render_template('table1.html',n=number)

@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
	return render_template("file_upload.html")

@app.route("/success", methods=['GET','POST'])
def success():
	if request.method == "POST":
		f=request.files['Akshay']
		f.save(f.filename)
		return render_template("success.html",f_name=f.filename)

@app.route("/email",methods=['POST','GET'])
def email_send():
	return render_template("email.html")
@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
	email=request.form['email']
	msg=Message("One Time Password", sender="n151248@rguktn.ac.in", recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template("v_email.html")
@app.route("/email_success",methods=['POST','GET'])
def success_email():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		return render_template("email_success.html")
	return "In valid OTP"

@app.route("/show")
def showData():
	register=session.query(Register).all()
	return render_template('show.html',reg=register)

@app.route("/form_db")
def form_db():
	return render_template("form_db.html")
@app.route("/edit")
def edit():
	return render_template("edit.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/new",methods=['POST','GET'])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			surname=request.form['surname'],
			mobile=request.form['mobile'],
			email=request.form['email'],
			branch=request.form['branch'],
			role=request.form['role'])
		session.add(newData)
		session.commit()
		flash("New Data Added {}".format(newData.name))
		return redirect(url_for('showData'))
	else:	
		return render_template('form_db.html')

@app.route("/",methods=['POST','GET'])
def navbar():
	return render_template("navbar.html")

@app.route("/",methods=['POST','GET'])
def index():
	return render_template("index.html")


@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editedData.name=request.form['name']
		editedData.surname=request.form['surname']
		editedData.mobile=request.form['mobile']
		editedData.email=request.form['email']
		editedData.branch=request.form['branch']
		editedData.role=request.form['role']

		session.add(editedData)
		session.commit()

		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)


@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(deletedData)
		session.commit()
		flash("Record Deleted {}".format(deletedData.name))

		return redirect(url_for('showData'))
	else:
		return render_template('delete.html',register=deleteData)



if __name__=='__main__':
	app.run(debug=True)
