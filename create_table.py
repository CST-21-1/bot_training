import sqlalchemy as db

engine = db.create_engine('sqlite:///tasks-sqlalchemy.db')

connection = engine.connect()

metadata = db.MetaData()

users = db.Table('Users', metadata,
    db.Column)




    # association
    # users = sa.orm.relationship('TopicUser', back_populates='topic')


main_engine = db.create_engine(
    'postgres://localhost:5432/habr_sql?sslmode=disable',
    echo=True,
)