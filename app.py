from flask import Flask, render_template,request,redirect,url_for,session
from flask_session import Session
import datetime
import database

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods = ["GET"])
def main():
        return render_template('index.html')





@app.route("/index", methods = ["POST"])
def index():

        
        exixting_user = database.users.find_one({"email" : request.form.get("email")})
        passwd = request.form.get("password")

        if exixting_user == None:
            return redirect(url_for("not_found"))
        else:
            if passwd == exixting_user["password"]:
                session["email"] = exixting_user["email"]
                return redirect(url_for("site_get"))
            else:
                return redirect(url_for("wrong_pass"))


@app.route("/wrong_pass",methods = ["GET"])
def wrong_pass():
    return render_template("wrong_pass.html")

            

@app.route("/site_get", methods=["GET"])
def site_get():
    email = session.get("email")
    entries = database.data.find_one({"email":email})

    if entries == None:
        entries = []
        database.data.insert_one({"email": email,"entries":entries})
        return render_template("site.html",email=email)
    else:
        entries = entries["entries"]
        return render_template("site.html",entries=entries)


            
@app.route("/site", methods=["POST"])
def site():
    
    email = session.get("email")
    entries = database.data.find_one({"email":email})

    if request.method == "POST" and email != -1:
        content = request.form.get("content")
        date = datetime.datetime.today().strftime("%Y-%m-%d")
        now = datetime.datetime.now()
        time = now.strftime("%H:%M:%S")

        database.data.find_one_and_update({"email":email},{"$push" :{"entries":{"date" : date,"content":content, "time":time}}})

        return redirect(url_for("site_get"))
    else:
        return redirect(url_for("main"))



@app.route("/not_found",methods = ["GET"])
def not_found():
    return render_template("not_found.html")



@app.route("/signin_get",methods = ["GET"])
def signin_get():
    return render_template("signin.html")


@app.route("/already", methods =["GET"])
def already():
    return render_template("already.html")



@app.route("/signin",methods = ["POST"])
def signin():

    email = request.form.get("email")
    user = database.users.find_one({"email": email})

    if user == None:
        database.users.insert_one(
        {
            'name': request.form.get("first_name"),
            'l_name' : request.form.get("second_name"),
            'password' : request.form.get("password"),
            'email' : email
        })
        return redirect(url_for("signedup_get"))
    else:
        return redirect(url_for("already"))


@app.route("/signedup_get",methods = ["GET"])
def signedup_get():
    return render_template("signedup.html")

@app.route("/about")
def about():
    return render_template("about_mydiary.html")

@app.route("/logout",methods = ["GET"])
def logout():
    session.clear()
    session["email"] = -1
    return redirect(url_for("main"))

@app.route("/delete/<string:date>,<string:time>", methods = ["GET"])
def delete(date,time):
    print("ritik")
    print(date)
    print(time)

    email = session.get("email")

    database.data.update({"email":email},{"$pull" : {"entries":{"date":date,"time":time}}})
    return redirect(url_for("site_get"))



    