import sqlite3 as sql
from flask import Flask,render_template,flash,session,request,redirect,url_for,get_flashed_messages
app = Flask(__name__)

####admin-credentials####
username='admin'
passwordu='admin'
####admin-credenials####

####dealer-credentials####
d_namee="Ckart"
d_username='dealer'
d_password='dealer'
####dealer-credentials####


app.secret_key = 'random string'

####index####
@app.route('/')
def index():
    return redirect(url_for('signout'))
    # return render_template('index.html')
####index####


####gallery####
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')
####gallery####


####products####
@app.route('/product',methods=['GET','POST'])
def product():
    if request.method=='POST':
        try:
            name=request.form["pname"]
            pice=request.form["price"]
            with sql.connect("cafe.db") as con:
                cur=con.cursor()
                cur.execute("INSERT INTO product (p_name,p_price) VALUES(?,?)",(name,pice))
                con.commit()
        except:
            con.rollback()
        finally:
            return redirect(url_for('list'))
            con.close()
####products####


####reservation####
@app.route('/orders')
def orders():
    return render_template('reservation.html')
####reservation####


@app.route('/order',methods=['GET','POST'])
def order():
    return redirect(url_for('orders'))

####menu####
@app.route('/menu')
def menu():
    return render_template('menu.html')
####menu####

####sigin####
@app.route('/sign',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        if request.form['email'] == username and request.form['password'] == passwordu:
            return redirect(url_for('list'))
        if request.form['email'] == d_username and request.form['password'] == d_password:
            return render_template('blog-detail.html')
        with sql.connect("cafe.db") as con:
            cur=con.cursor()
            cur.execute("select * from customer where email=?",[email])
            con.commit()
            user=cur.fetchone()
            cur.close()
            if len(user)>0:
                if request.form['password']==user[4]:
                    session['name']=user[1]
                    session['email']=user[3]
                    curr=con.cursor()
                    curr.execute("update customer set status=1,flag=1 where email=?", [email])
                    con.commit()
                    curr.close()
                    return redirect(url_for('menu'))
####sigin####


####signout####
@app.route('/signout')
def signout():
    with sql.connect("cafe.db") as con:
        cur=con.cursor()
        cur.execute("update customer set flag=0 where status=1")
        con.commit()
        cur.close()
    session.clear()
    return render_template("index.html")
####signout####


@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        return render_template('reg.html')

####signup####
@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method=='POST':
        try:
            name=request.form['name']
            phone=request.form['phone']
            ema=request.form['email']
            pswd=request.form['password']
            status=0
            flag=0
            with sql.connect("cafe.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO customer (name,phone,email,password,status,flag) VALUES(?,?,?,?,?,?)",(name,phone,ema,pswd,status,flag))
                con.commit()
        except:
            con.rollback()
        finally:
            return render_template('index.html')
            con.close()
####signup####

####ORDERE_ITEMS####
@app.route('/order_items',methods=['GET','POST'])
def order_items():
    if request.method=='POST':
        try:
            n=request.form['pn']
            l=request.form['pr']
            m=request.form['qt']
            with sql.connect("cafe.db") as con:
                flag=1
                cur=con.cursor()
                cur.execute("INSERT INTO order_items(user_id,product_id,total_price,no_items,flag) VALUES ((select id from customer where flag=1),(select p_id from product where p_name=? ),?,?,?)",(n,l,m,flag))
                con.commit()
                cur.close()
                curr=con.cursor()
                curr.execute("INSERT INTO dealer(d_name,d_oid,d_flag) VALUES (?,(select order_id from order_items where flag=1),?)",(d_namee,flag))
                con.commit()
                curr.close()
                cur1=con.cursor()
                cur1.execute("UPDATE order_items set flag=0")
                con.commit()
                cur1.close()

        except:
            con.rollback()
        finally:
            return render_template("blog.html")
            con.close()
####ORDERE_ITEMS####

####LAST_DEAL####
@app.route('/curdeals',methods=['GET','POST'])
def curdeals():

    con=sql.connect("cafe.db")
    con.row_factory=sql.Row

    cur=con.cursor()
    cur.execute("select * from dealer ORDER BY d_id DESC LIMIT 1")

    rows = cur.fetchall()
    return render_template("blog-detail.html",rows = rows)
####LAST_DEAL####


####ALL_DEALS####
@app.route('/d_list',methods=['GET','POST'])
def d_list():
    con=sql.connect("cafe.db")
    con.row_factory=sql.Row

    cur=con.cursor()
    cur.execute("select * from dealer")

    rows = cur.fetchall()
    return render_template("blog-detail.html",rows = rows)
####ALL_DEALS####

####PRODUCT_TAKEN_BY_CUSTOMER####
@app.route('/list2',methods=['GET','POST'])
def list2():

        con = sql.connect("cafe.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        if request.form['na']:
            cur.execute("select * from product LIMIT 1 OFFSET ?",[request.form.get('na')])
            rows = cur.fetchall()
            return render_template("reservation.html",rows = rows)
####PRODUCT_TAKEN_BY_CUSTOMER####

####PRODUCT_DETAILS####
@app.route('/list1',methods=['GET','POST'])
def list1():
    con = sql.connect("cafe.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from product")

    rows = cur.fetchall()
    return render_template("about.html",rows = rows)
####PRODUCT_DETAILS####


####CUSTOMER_DETAILS####
@app.route('/list')
def list():
    con = sql.connect("cafe.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from customer")

    rows = cur.fetchall()
    return render_template("about.html",rows = rows)
####CUSTOMER_DETAILS####


if __name__=='__main__':
    app.run(debug=True)