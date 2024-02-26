from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Todo(BaseModel):
  # id: int
  content: str
  is_important: bool = False


while True:
  try:
    conn = psycopg2.connect(host='localhost', database='Todo',
                            user='postgres', password='HABSIDFAG')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print("Yay, Connected Successfully")
    break

  except Exception as error:
    print("Connection was failed:")
    print("Error: ", error)
    time.sleep(5)


@app.get("/")
def root():
  return dict(Msg='this is root api')


@app.get("/todo")
def get_todos():

  cursor.execute("""SELECT * FROM todos""")
  todos = cursor.fetchall()

  return todos


@app.post("/todo")
def create_todos(new_todo: Todo):

  cursor.execute(""" INSERT INTO todos (content, is_important) VALUES (%s, %s) RETURNING * """,
                 (new_todo.content, new_todo.is_important))
  created_todo = cursor.fetchone()
  conn.commit()

  return created_todo


@app.get("/todo/important")
def get_imp_todos():
  cursor.execute("""SELECT * FROM todos WHERE is_important = true""")
  todos = cursor.fetchall()

  return todos


@app.delete("/todo/{id}")
def delete_post(id: int):
  cursor.execute(
      """DELETE FROM todos WHERE id = (%s) RETURNING * """, (str(id)))
  cursor.fetchone()
  conn.commit()

  return None
