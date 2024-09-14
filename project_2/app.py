from flask import Flask,render_template,session,redirect,url_for,request,flash
from flask_mysqldb import MySQL
import re
app=Flask(__name__)
app.secret_key="123qwe"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='familylove@26'
app.config['MYSQL_DB']='empdetails'

mysql= MySQL(app)


    
def validate_password(password):
    if len(password)<8:
        return False
    elif not re.search (r"[a-z]",password):
        return False
    elif not re.search(r"[A-Z]",password):
        return False
    elif not re.search(r"[0-9]",password):
        return False
    elif not re.search(r"[!@#$%^&*+=]",password):
        return False
    return True
    
def loggedin():
    return "username" in session

@app.route("/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if not validate_password(password):
            flash('Password should be at least 8 characters long and contain uppercase, lowercase, digit, and special characters.', 'danger')
            return redirect(url_for("signup"))
        cur=mysql.connection.cursor()
        cur.execute("insert into emp_pswrd(username,password) values(%s,%s)",(username,password))
        mysql.connection.commit()
        cur.close()
        flash("signup successful",'success')
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")

        cur=mysql.connection.cursor()
        cur.execute("select * from emp_pswrd where username=%s",(username,))
        data=cur.fetchone()
        cur.close()
        if data[0]==username and data[1]==password:
            session["username"]=username
            flash("login successful")
            return redirect(url_for("display"))
           
        else:
            flash("invalid username",'danger')
             
    return render_template("login.html")

@app.route("/home")
def display():
   
    return render_template("home.html")




@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute("delete from emp_pswrd where id=%s",(id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("login.html"))


        

if __name__=="__main__":
    app.run(debug=True)