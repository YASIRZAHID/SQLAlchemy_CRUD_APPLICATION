from ast import Return
from datetime import datetime
from email.policy import default
from flask import Flask, Request, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyProject.db'
app.config['SQLALCHEMY_TRACK_MODIFCATIONS'] = False
db = SQLAlchemy(app)

class MyProjects(db.Model):
    Sno =     db.Column(db.Integer , primary_key = True)
    project = db.Column(db.String(200) , nullable = False)
    description =   db.Column(db.String(500) , nullable = False)
    Dated =   db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.project}"


@app.route('/' , methods=['GET' , 'POST'])
@app.route('/hello')
def HelloWorld():
    if request.method == 'POST':
        getproject=      request.form.get('project')
        getdescription=  request.form.get('description')
        getDated=        request.form.get('date')

        myprojects = MyProjects(project = getproject , description = getdescription)
        db.session.add(myprojects)
        db.session.commit()

    allmyprojects = MyProjects.query.all()
    return render_template('index.html' , allmyprojects=allmyprojects)


@app.route('/show')
def Products():
    allmyprojects = MyProjects.query.all()
    print(allmyprojects)
    return "I AM SHOW"

@app.route('/delete/<int:Sno>')
def delete(Sno):
    allmyprojects = MyProjects.query.filter_by(Sno=Sno).first()
    db.session.delete (allmyprojects)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:Sno>' , methods=['GET' , 'POST'])
def update(Sno):
    if request.method == 'POST':
        getproject=      request.form.get('project')
        getdescription=  request.form.get('description')

        allmyprojects = MyProjects.query.filter_by(Sno=Sno).first()
        allmyprojects.project = getproject
        allmyprojects.description = getdescription
        db.session.add(allmyprojects)
        db.session.commit()
        return redirect("/")
    allmyprojects = MyProjects.query.filter_by(Sno=Sno).first()
    return render_template('update.html' , allmyprojects=allmyprojects)
    return "UPDATED SUCCESSFULLY"        

if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0' , port= 8000)
