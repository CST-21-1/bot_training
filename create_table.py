import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

engine = db.create_engine('sqlite:///tasks-sqlalchemy.db', echo=True)
Session = sessionmaker(bind=engine)
connection = engine.connect()

metadata = db.MetaData()

users = db.Table('users', metadata,
                 db.Column('user_id', db.Integer, db.Sequence("user_id_seq"), primary_key=True),
                 db.Column('chat_id', db.Integer)
                 )

tasks = db.Table('tasks', metadata,
                 db.Column('task_id', db.Integer, db.Sequence("task_id_seq"), primary_key=True),
                 db.Column('user_id', db.Integer),  # , foreign_key='users.user_id')
                 db.Column('name', db.Text),
                 db.Column('description', db.Text),
                 db.Column('deadline', db.DateTime)
                 )

metadata.create_all(engine)