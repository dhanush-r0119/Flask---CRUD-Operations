from flask import *
import sqlite3


app =Flask(__name__)
app.secret_key="123" 

con=sqlite3.connect("database.db")
con.execute("CREATE TABLE IF NOT EXISTS data(pid INTEGER PRIMARY KEY, name TEXT, address TEXT, contact INTEGER, mail TEXT)")
con.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_record')
def add_record():
    return render_template('add_record.html')

@app.route('/add_data',methods=['POST','GET'])
def add_data():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("INSERT INTO data(name,address,contact,mail)values(?,?,?,?)",(name,address,contact,mail))
            con.commit()
            flash("Record Added Succesfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("home"))
            con.close()


@app.route('/view_record')
def view_record():
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM data")
    data=cur.fetchall()
    con.close()
    return render_template("view_record.html",data=data)

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM data WHERE pid=?",(id))
    data=cur.fetchone()
    con.close()

    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("UPDATE data SET name=?,address=?,contact=?,mail=? where pid=?",(name,address,contact,mail,id))
            con.commit()
            flash("Update successfully","success")

        except:
            flash("Error in Update operation","danger")
        finally:
            return redirect(url_for('home'))

    return render_template('update.html',data=data)


@app.route('/delete/<string:id>')
def delete(id):
    try:
        con=sqlite3.connect("database.db")
        cur=con.cursor()
        cur.execute("DELETE FROM data WHERE pid=?",(id))
        con.commit()
        flash("Record deleted successfully","success")
    except:
        flash("Record delete failed","danger")
    finally:
        return redirect(url_for("home"))
        con.close()


if __name__=='__main__':
    app.run(debug=True)