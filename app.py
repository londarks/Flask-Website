import flask
import base64
from flask import Flask,request, jsonify, render_template, redirect, url_for
from Controller import main

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False


#controladores do site
Controller = main.WebsiteControl()

def cookie():
	login = request.cookies.get('Athus-session')
	return login


#rotas
@app.route("/")
def index():
	""" pagina inicial com autentificação de cookie """
	users = Controller.reload()
	login = cookie()
	return render_template("index.html", usuarios=users, cookie=login)

@app.route("/dashbord")
def dashbord():
	""" pagina dos adm """
	login = cookie()
	if login != None:
		info = Controller.reload()
		blacklist = Controller.blacklist()
		usr = Controller.Dashboard()
		admin = Controller.adminstrator()
		adminOnline = Controller.adminOnline()
		time_online = Controller.timeOnline()
		cache = request.cookies.get('Athus-acess')
		return render_template("dashbord.html", time_online=time_online,
			                                    Onlineusr=info,
			                                    cookie=login,
			                                    blacklist=blacklist,
			                                    Online=usr,
			                                    admin=admin,
			                                    admns=adminOnline,
			                                    cache=cache)
	return redirect(url_for(".login"))

#name
#tripcode

@app.route("/commands/")
def commands():
	""" pagina inicial com autentificação de cookie """
	login = cookie()
	return render_template("commands.html",cookie=login)

@app.route("/login/")
def login():
	""" pagina inicial com autentificação de cookie """
	return render_template("login.html")

@app.route("/register/", methods = ['POST'])
def register():
	user = request.form['username']
	password = request.form['password']
	register = Controller.register(user, password)
	res = flask.make_response()
	res.headers['location'] = url_for('login')
	return res, 302

@app.route("/logout/")
def logout():
	""" logout """
	res = flask.make_response()
	res.delete_cookie("Athus-session")
	res.delete_cookie("Athus-acess")
	res.headers['location'] = url_for('index')
	return res, 302

@app.route("/cadastro/")
def cadastro():
	""" pagina inicial com autentificação de cookie """
	return render_template("cadastro.html")


# @app.route("/update/", methods = ['POST'])
# def update():
# 	""" update itens website """
# 	msg = request.args.get('menssage')
# 	Controller.setupdate(msg)
# 	return ""

@app.route("/punishments/", methods = ['POST'])
def punishments():
	""" kick player"""
	if 'kick' in request.form:
		userID = request.form['kick']
		#banindo usuario
		Controller.kick(userID)
		return redirect(url_for(".dashbord"))
	elif 'ban' in request.form:
		userID = request.form['ban']
		#kikando usuario
		Controller.ban(userID)
		return redirect(url_for(".dashbord"))
	elif 'blacklist' in request.form:
		userID = request.form['blacklist']
		Controller.insetBlacklist(userID)
		return redirect(url_for(".dashbord"))
	elif 'unblock' in request.form:
		userID = request.form['unblock']
		Controller.deleteBlacklis(userID)
		return redirect(url_for(".dashbord"))
	

@app.route("/oauth/", methods = ['POST'])
def oauthlogin():
	user = request.form['username']
	password = request.form['password']
	check = Controller.checkLogin(user, password)
	if check == "invalid":
		error = "name or password is incorrect"
		return render_template("login.html", error=error)
	res = flask.make_response()
	res.set_cookie("Athus-session", value=check[0])
	res.set_cookie("Athus-acess", value=check[1])
	res.headers['location'] = url_for('dashbord')
	return res, 302


@app.route("/not_authorized/")
def not_authorized():
    """pagina de não autorizado"""
    return render_template('401.html')


@app.errorhandler(404)
def page_not_found(e):
    """Page Not found"""
    return render_template('404.html'),404

@app.errorhandler(405)
def method_not_allowed(e):
    """Page Not found"""
    return render_template('404.html'),405 

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
