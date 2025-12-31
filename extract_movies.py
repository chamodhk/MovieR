import re 
from sqlalchemy import create_engine, select 
from sqlalchemy.orm import sessionmaker
from gliner import GLiNER
from models import Comment, Movie, CommentMovie
model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
labels = ["Movie", "TV Series"]


BAD_PATTERNS = [
    r"tt\d+",
    r"[A-Za-z]:\\Users",
    r"^\d+$",
    r"^\w{1,2}$",
]

BLACKLIST = {"movie"}

def is_bad_pattern(text):
    for pattern in BAD_PATTERNS:
        if re.match(pattern, text):
            return True
    return False

def filter_entities(entities):
    clean = set()
    for en in entities:
        name = en["text"].strip().lower()

        if name in BLACKLIST:
            continue
        if is_bad_pattern(name):
            continue

        clean.add(name.title())
    return clean


engine = create_engine("sqlite:///output.db", future=True)
Session = sessionmaker(bind=engine)
session = Session()

BATCH_SIZE = 100
offset = 0
processed = 0

while True:
    comments = session.execute(
        select(Comment)
        .order_by(Comment.id)
        .offset(offset)
        .limit(BATCH_SIZE)
    ).scalars().all() 

    if not comments:
        break 

    for comment in comments:
        if not comment.body:
            continue 

        entities = model.predict_entities(
            comment.body,
            labels,
            threshold=0.5
        )

        movies = filter_entities(entities)

        for movie_name in movies:
            movie = session.execute(
                select(Movie).where(Movie.name == movie_name)
            ).scalar_one_or_none()

            if not movie:
                movie = Movie(name=movie_name)
                session.add(movie)
                session.flush()

            link = CommentMovie(
                comment_id = comment.id,
                movie_id = movie.id 
            )

            session.merge(link)


        processed += 1

    session.commit()
    offset += BATCH_SIZE

    print(f"Processed {processed} comments")

session.close()
print("Extraction complete!")


