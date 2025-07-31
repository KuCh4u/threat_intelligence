from sqlalchemy import create_engine
from app.models import Base

engine = create_engine('sqlite:///threatintel.db')

Base.metadata.create_all(engine)

print("Base de datos creada con éxito.")
