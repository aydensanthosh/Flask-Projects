from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#My app
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///Personal-Expense-Tracker.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

def init_db():
    with app.app_context():
        db.create_all()
    
class Expenses(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    amount=db.Column(db.Numeric(10,2),nullable=False)
    description=db.Column(db.String(200))
    category=db.Column(db.String(50),nullable=False)
    payment_method=db.Column(db.String(50),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id % self.category

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=="POST":
        expense_amount=request.form['amount']
        expense_desc=request.form['description']
        expense_category=request.form['category']
        expense_payment=request.form['payment_method']
        New_Expense=Expenses(amount=expense_amount,description=expense_desc,category=expense_category,payment_method=expense_payment)
        try:
            db.session.add(New_Expense)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"there was an error {e}"
    else:
        expense=Expenses.query.all()
        return render_template("index.html",expenses=expense)

@app.route('/delete/<int:id>')
def delete(id):
    Mistake=Expenses.query.get_or_404(id)
    try:
        db.session.delete(Mistake)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"Some problem deleteing error, Error is :{e}"

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    Updatee=Expenses.query.get_or_404(id)
    if request.method=='POST':
        Updatee.amount=request.form['amount']
        Updatee.description=request.form['description']
        Updatee.category=request.form['category']
        Updatee.payment_method=request.form['payment_method']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Some trouble Updating: {e}"
    else:
        return render_template('update.html',expense=Updatee)
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    
