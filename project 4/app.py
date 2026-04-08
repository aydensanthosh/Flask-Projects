from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#My app
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///To-Do_Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

with app.app_context():
    db.create_all()
    
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task_name=db.Column(db.String(200),nullable=False)
    task_complete=db.Column(db.Integer,default=1)
    task_created=db.Column(db.DateTime,default=datetime.now)

    #When print the object the Object ID will be printed
    def __repr__(self)-> str:
        return f"Task ({self.id}):{self.task_name}"
    



@app.route("/",methods=["POST","GET"])
def index():
    #Add a Task
    if request.method == "POST": #When something is passed on from the html page
        current_task=request.form['content'] 
        new_task=Task(task_name=current_task) #creating an object with task name as the one sent from html page
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error : {e}")
            return f"Error :{e}"
    else:
        tasks=Task.query.order_by(Task.task_created).all()
        return render_template("index.html",tasks=tasks)  
    #See current all tasks

    #See all completed Tasks


    return render_template("index.html")


#Deleting a task.
@app.route('/delete/<int:id>')
def delete(id:int):
    delete_task=Task.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}\nTask Not found"

#Editing an existing task
@app.route('/edit/<int:id>',methods=["POST","GET"])
def edit(id):
    editing_task=Task.query.get_or_404(id)
    if request.method=="POST":
        editing_task.task_name=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error : {e}"
    else:
        return render_template('edit.html',task=editing_task)

@app.route('/complete/<int:id>')
def complete(id):
    task=Task.query.get_or_404(id)
    if task.task_complete==0:
        task.task_complete=1
    else:
        task.task_complete=0
    try:
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Error: {e}"
        




if __name__ == "__main__":
    app.run(debug=True)
