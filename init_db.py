import sqlite3

connection = sqlite3.connect('todo.db')

with open('schema.sql') as f:
    connection.executescript(f.read())


cur = connection.cursor()

cur.execute("INSERT INTO todos (name, status) values ('learning flask','new')")
cur.execute("INSERT INTO todos (name, status) values ('react redux','complete')")

connection.commit()

connection.close()