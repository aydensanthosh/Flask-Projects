from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request ,redirect
from datetime import datetime
# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///To-Do-app.db'
db=SQLAlchemy(app)

def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database created!")

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    due_date=db.Column(db.DateTime,nullable=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

# Define a route - this is the homepaged
@app.route('/',methods=['POST','GET'])
def index():
    if request.method=="POST":
        task_content=request.form['content']
        task_due_date=request.form['date']
        task_due_date = datetime.strptime(task_due_date, '%Y-%m-%d')
        new_task=Todo(content=task_content,due_date=task_due_date)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task!!!"
    else:
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)

# route to deleting an item
@app.route('/delete/<int:id>')
def delete(id):
    tasks_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(tasks_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return f"There was a problem deleting the task {id}"  

# route to update an item
@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task_to_update=Todo.query.get_or_404(id)
    if request.method=='POST':
        task_to_update.content=request.form['content']
        task_to_update.due_date=datetime.strptime(request.form['date'], '%Y-%m-%d')
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return(f"Some problem while updating:\n{e}")
    else:
        return render_template('update.html',task=task_to_update)


# Run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)  # debug=True auto-reloads on code changes