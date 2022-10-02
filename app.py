from flask import Flask, render_template,request,session
import sqlite3 as sql
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = '12331243112'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

@app.route('/')
def new_user():
    return render_template('login.html')

@app.route('/signup',methods = ['POST', 'GET'])
def sign():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            user_pw = request.form['user_pw']
            with sql.connect("database.db") as con:
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
            with sql.connect("database.db") as con:
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

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from users")

    rows = cur.fetchall()
    return render_template("list.html",rows = rows)

@app.route('/result')
def restul():
    return render_template("result.html")
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)