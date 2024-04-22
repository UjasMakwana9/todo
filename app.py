from flask import *
from flask import render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

class todo(db.Model):
    sr = db.Column(db.Integer,primary_key=True)
    val = db.Column(db.String(200),nullable=False)

    def __repr__(self) -> str:
        return f"{self.sr} - {self.val}"

@app.route('/')
def origin(error=None):
    
    all_data = todo.query.all()
    print(all_data)
    if error == "":
        return render_template('index.html',all_data=all_data)
    
    return render_template('index.html',all_data=all_data,error=error)

@app.route('/submit',methods=['GET','POST'])
def fun():
    error = None
    if request.method=='POST':
            if request.form['val']=="":

                error = "Null Value"
                return origin(error)
            else:     
                value = todo(val=request.form['val'])
                db.session.add(value)
                db.session.commit()
                return redirect('/')
    else:
        return redirect('/')

@app.route('/dele/<int:sr>',methods=['GET','POST'])
def dele(sr):
    to = todo.query.filter_by(sr=sr).first()
    db.session.delete(to)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sr>',methods=['GET','POST'])
def update(sr):
        if request.method=="POST":
            val=request.form['val']
            to = todo.query.filter_by(sr=sr).first()
            to.val = val
            db.session.add(to)
            db.session.commit()
            return redirect('/')
        else:
            to= todo.query.filter_by(sr=sr).first()
            return render_template('update.html',to=to)




if __name__=="__main__":
    app.run(debug=True,port=2000)