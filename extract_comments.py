""""
    This file exracts all the comments from the MovieSuggestions_comments file and store it
    in the output db (SQLite) database.

    I only stored three fields from the comment; score, parent_id and the body of the comment

"""



import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Comment 

INPUT = "MovieSuggestions_comments"
DB_URL = "sqlite:///output.db"

engine = create_engine(DB_URL, future=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session() 

BATCH_SIZE = 10000
batch = []

FIELDS = ["score", "parent_id", "body"]

parents = set()
count = 0

with open(INPUT, "r", encoding='utf-8') as infile:
    for line in infile:
        try:
            obj = json.loads(line)
            batch.append(
                Comment(
                    score=obj.get("score"),
                    parent_id=obj.get("parent_id"),
                    body=obj.get("body")
                )
            )

            if len(batch) >= BATCH_SIZE:
                session.bulk_save_objects(batch)
                session.commit()
                batch.clear()
                print("a batch completed")

        except json.JSONDecodeError:
            continue

if batch:
    session.bulk_save_objects(batch)
    session.commit()
    batch.clear()

session.close()
