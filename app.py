from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

app = Flask(__name__)


# 设置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_info = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)


def table_exists(table_name):
    """
    检查数据表是否存在
    """
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()


# 创建数据库表
with app.app_context():
    if not table_exists("todo"):
        print(f'创建新表......')
        db.create_all()


@app.route('/', methods=["GET"])
def index():
    """
    主页面
    """
    tasks = Todo.query.all()
    task_list = [[task.id, task.task_name, task.task_info, task.completed] for task in tasks]
    return render_template("index.html", tasks=task_list)


@app.route("/add_mission", methods=["POST", "GET"])
def add_mission():
    """
    添加任务
    """
    if request.method == "POST":
        # 从请求中获取数据
        task_name = request.form['task-name']
        task_info = request.form['task-info']
        print(task_name)
        print(task_info)

        # 创建新的待办事项
        new_todo = Todo(task_name=task_name, task_info=task_info, completed=False)

        # 添加到数据库会话
        db.session.add(new_todo)

        # 提交更改
        db.session.commit()

        return redirect(url_for('index'))
    return render_template("add_mission.html")


@app.route('/delete/<int:todo_id>', methods=["POST"])
def delete_todo(todo_id):
    """
    删除任务
    """
    todo  = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"success": True, "redirect": url_for('index')})


@app.route('/complete/<int:todo_id>', methods=["POST"])
def complete_todo(todo_id):
    """
    标记任务完成状态
    """
    todo = Todo.query.get_or_404(todo_id)
    todo.completed = True
    db.session.commit()
    return jsonify({"success": True, "redirect": url_for('index')})


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )






