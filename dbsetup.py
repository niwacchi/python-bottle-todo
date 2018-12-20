import sqlite3
conn = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
conn.execute("INSERT INTO todo (task,status) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
conn.execute("INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
conn.execute("INSERT INTO todo (task,status) VALUES ('Test various editors for and check the syntax highlighting',1)")
conn.execute("INSERT INTO todo (task,status) VALUES ('Choose your favorite WSGI-Framework',0)")
conn.execute("CREATE TABLE user ( id INTEGER PRIMARY KEY, username char(100) NOT NULL, password char(100) NOT NULL )")
conn.execute("INSERT INTO user ( username, password ) VALUES ('test01', 'pass01')")
conn.commit()

