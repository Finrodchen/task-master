from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__) #__name__目前執行的模組
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    priority = db.Column(db.String(200), nullable = False)
    content = db.Column(db.String(200), nullable = False)
    people = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_priority = request.form['priority']
        task_content = request.form['content']
        task_people = request.form['people']
        new_task = Todo(priority=task_priority, content=task_content, people=task_people)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Fail to add new issue to your task."    
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    
    except:
        return "Deleteing problem."

@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.priority = request.form['priority']
        task.content = request.form['content']
        task.people = request.form['people']

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "Updating issue."
    else:
        return render_template('update.html', task=task)

if __name__=="__main__": #如果以上程式執行
    app.run() #執行app
