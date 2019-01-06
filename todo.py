import sqlite3
from bottle import route, run, debug, template, request, static_file, error, redirect, static_file
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
 
engine = create_engine('sqlite:///todo.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)

class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    task = Column(String(100))
    status = Column(Boolean)

    def __repr__(self):
        return "<Todo(id='%s', task='%s', score='%s')>" % (self.id, self.task, self.status)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))

@route('/')
def index():
    return template("templates/index")

@route('/login')
def login():
    return template("templates/login")

@route('/login', method="POST")
def do_login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User).filter(User.username==username).filter(User.password==password)

    if(result.count() > 0):
        redirect('/todo')


@route('/todo')
@route('/my_todo_list')
def todo_list():

    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(Todo.id, Todo.task).filter(Todo.status=='1').all()

    return template('templates/make_table', rows=result)

@route('/new', method='GET')
def new_item():
    if request.GET.save:
        new = request.GET.task.strip()

        t = Todo(task=new,status=1)

        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(t)
        session.flush()
        session.commit()

        return '<p>The new task was inserted into the database, the ID is %s</>' % t.id
    else:
        return template('templates/new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):
    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        Session = sessionmaker(bind=engine)
        session = Session()
        t = session.query(Todo).filter_by(id=no).one()
        t.task = edit
        t.status = status
        session.add(t)
        session.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchone()

        return template('templates/edit_task', old=cur_data, no=no)


@route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    c.close()
    if not result:
        return 'The item number dose note exist!'
    else:
        return 'Task: %s' % result[0]


@route('/help')
def help():
    return static_file('help.html', route='/path/to/file')


@route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'The parameter you passed has the wrong format!'


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


debug(True)
run(host='127.0.0.1', port=8080, reloader=True)
