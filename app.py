from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog")
with mysql.connector.connect(host="localhost",user="root",password="system",database="flaskblog"):
     cursor=mydb.cursor(buffered=True)
     cursor.execute("create table if not exists registration(Username varchar(50) primary key,mobile varchar(50) unique,address varchar(50),email varchar(50) unique,password varchar(50))")
     cursor.execute("create table if not exists login(Username varchar(30) primary key,password varchar(30))")
app=Flask(__name__)
app.secret_key="my secretkey is too secret"
@app.route('/')
def home():
    return  render_template("homepage.html")
@app.route('/reg',methods=['GET','POST'])
def register():
    if request.method=='POST':
        Username=request.form['Username']
        mobile=request.form['mobile']
        address=request.form['address']
        email=request.form['email']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into registration values(%s,%s,%s,%s,%s)',[Username,mobile,address,email,password])  
        mydb.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('registration.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        Username=request.form['Username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from registration where Username=%s && password=%s',[Username,password])  
        data=cursor.fetchone()[0]
        print(data)
        cursor.close()
        if data==1:
            session['username']=Username
            if not session.get(session['Username']):
                session[session['Username']]={}       
            return redirect(url_for('home'))
        else:
            return "Invalid Credentails"
    return render_template('login.html')
@app.route('/logout')
def logout():
    if session.get('Username'):
        session.pop('Username') 
    return redirect(url_for('login'))       
@app.route('/admin')
def admin():
    return render_template('admin.html') 
@app.route('/addposts',methods=['GET','POST'])
def addposts():
    if request.method=='POST':
        title=request.form.get('title')
        content=request.form.get('content')
        slug=request.form.get('slug')
        print(title)
        print(content)
        print(slug)
        cursor=mydb.cursor(buffered=True)
        cursor.execute('INSERT INTO posts(title,content,slug) VALUES(%s,%s,%s)',(title,content,slug))
        mydb.commit()
        cursor.close()
    return render_template('add_post.html') 
@app.route('/viewpost') 
def viewpost():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts')
    posts=cursor.fetchall()
    print(posts)
    cursor.close()
    return render_template('viewpost.html',posts=posts) 
@app.route('/delete_post/<int:id>',methods=['POST'])
def delete_post(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.execute('DELETE FROM posts WHERE id=%s',(id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('viewpost')) 
@app.route('/update_post/<int:id>',methods=['GET','POST'])
def update_post(id):
    if request.method=='POST':
        title=request.form.get('title')
        content=request.form.get('content')
        slug=request.form.get('slug')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('UPDATE posts SET title=%s,content=%s,slug=%s WHERE id=%s',(title,content,slug,id)) 
        mydb.commit()
        cursor.close()
        return redirect(url_for('viewpost'))
    else:
        cursor=mydb.cursor(buffered=True)
    cursor.execute('select * from posts where id=%s',(id,))
    post=cursor.fetchone()
    cursor.close()
    return render_template('update.html',post=post)           
app.run()                   


        
