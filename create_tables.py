from sqlalchemy import create_engine
from models import Base

engine = create_engine("sqlite:///output.db", future=True)

Base.metadata.create_all(engine)

print("Tables created")
