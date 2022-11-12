from sqlalchemy import create_engine

ENGINE = create_engine('mysql+mysqlconnector://root:root@localhost/todo', echo=True)
TOKEN = '5600387192:AAHpc1Nyt5NJQ6WzhadeB1uOZBBkEDEPjCU'