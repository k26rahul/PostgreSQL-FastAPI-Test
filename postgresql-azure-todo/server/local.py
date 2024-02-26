from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    # id: int
    content: str
    important: bool = False


@app.get("/")
def root():
    return dict(Msg='this is root api')


my_todos = [
    {"content": "this is a todo ex", "important": True, "id": 1},
    {"content": "this is also a todo ex2", "important": False, "id": 2}
]


def find_imp_todo():
    imp_todos = []
    for todo in my_todos:
        if todo["important"]:
            imp_todos.append(todo)
    return imp_todos


@app.get("/todo")
def get_todos():
    return dict(Msg=my_todos)


@app.get("/todo/important")
def get_imp_todos():
    important = find_imp_todo()
    return important


@app.post("/todo")
def create_todos(new_todo: Todo):
    # but now new_todo is not subscriptable as this is not a dict but pydantic model so we can use model_dump or this
    new_todo = dict(new_todo)
    new_todo["id"] = len(my_todos) + 1
    my_todos.append(new_todo)
    return dict(Msg=my_todos[-1])
