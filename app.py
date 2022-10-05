from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3 as sql
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '12331243112'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

@app.route('/')
def new_user():
    isSession = False
    try:
        if session['userId']:
            isSession = True
        else:
            isSession = False
    except:
        return render_template('main.html')
    finally:
        if isSession == True:
            return board()
        else:
            return render_template('main.html')

@app.route('/signup',methods = ['POST', 'GET'])
def sign():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            with sql.connect("login.db") as con:
                cur = con.cursor()  
                cur.execute("INSERT INTO users (id, pw) VALUES (?,?)",(user_id,user_pw) )
                msg = "Success"
        except:
            con.rollback()
            msg = "error"
        finally:
            return render_template("result.html",msg = msg)
    con.close()
    
@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        try:
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            with sql.connect("login.db") as con:
                cur = con.cursor()  
                cur.execute("select id from users where id=? and pw=?",(user_id,user_pw))
                result = cur.fetchall()
            if result[0][0] == user_id:
                session['userId'] = user_id
                session.permanent = True
                return render_template('result.html',msg=user_id)
            else:
                msg = "login fail"
                return render_template('result.html',msg=msg)
        except:
            con.rollback()
            msg = "login fail"
            return render_template('result.html',msg=msg)
    con.close()

@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')
    

@app.route('/list')
def list():
    con = sql.connect("login.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from users")

    rows = cur.fetchall()
    return render_template("list.html",rows = rows)

@app.route('/result')
def restul():
    return render_template("result.html")

@app.route('/board')
def board():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM Board")
    rows = cur.fetchall()

    for i in range(len(rows)):
        print(rows[i][0] + ':' + rows[i][1])
    return render_template("board1.html", rows = rows)

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        name = request.form["name"] 
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM Board WHERE name='{name}'")
        rows = cur.fetchall()
        print("DB : ")
        for i in range(len(rows)):
            print(rows[i][0] + ':' + rows[i][1])
        return render_template("search.html", rows=rows)
    else:
        return render_template("search.html")

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        try:
            name = request.form["name"]
            context = request.form["context"]

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Board(name,context) VALUES('{name}','{context}')")
                con.commit()
        except:
            con.rollback() 
        finally:
            return redirect(url_for("board"))
    else:
        return render_template("add.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)