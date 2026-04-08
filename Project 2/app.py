from flask import Flask ,render_template,redirect,url_for,request,session,flash
ADMIN_ACCESS=True
app=Flask(__name__)
app.secret_key= "Hello"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method=="POST":
        fname=request.form['fname']
        lname=request.form['lname']
        session['fname'],session['lname']=fname,lname
        return redirect(url_for("admin_name"))
    else:
        if 'fname' in session or 'lname' in session:
            return redirect(url_for(index))
        return render_template('admin.html')


@app.route('/admin_name')
def admin_name():
    if 'fname' in session and 'lname' in session:
        return f"<h1>Your name is {session['fname']} {session['lname']}\n\n\n<a href='/logout'>Logout?</a>"
    else:
        return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop("fname",None)
    session.pop('lname',None)
    flash("You have successfully Logged out!", category="Info")
    return redirect(url_for("index"))
if __name__=="__main__":
    app.run(debug=True)
    