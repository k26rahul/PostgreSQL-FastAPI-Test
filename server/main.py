from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{
    DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  email = Column(String, unique=True, index=True)


Base.metadata.create_all(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def check_db_connection():
  try:
    # Attempt to create a session
    session = SessionLocal()
    session.execute(text("SELECT 1"))
    session.close()
    print("Successfully connected to database.")
  except Exception as e:
    print(f"Failed to connect to database. Error: {e}")


# Call the function to check database connection
check_db_connection()


@app.get("/")
def read_root():
  return {"Hello": "World"}


@app.get("/db")
def read_users():
  try:
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return {"users": [{"id": user.id, "email": user.email} for user in users]}
  except Exception as e:
    return {"error": str(e)}
