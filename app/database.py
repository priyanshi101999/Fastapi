from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import setting

SQLALCHEMY_DATABASE_URL=f"postgresql+psycopg://{setting.database_username}:{setting.database_password}@{setting.database_hostname}:{setting.database_port}/{setting.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()


def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         connect = psycopg.connect(host='localhost', port=5432, dbname='FastAPI', user='postgres',password='root')
#         cursor = connect.cursor(row_factory=psycopg.rows.dict_row)
#         print("Connected to database successfully")
#         break;
#     except Exception as error:
#         print("Connection failed")
#         print("Error : ", error)
#         time.sleep(2)
