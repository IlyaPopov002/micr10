from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine_ord = create_engine(settings.postgres_url_ord, echo=True)
#engine_rec = create_engine(settings.postgres_url_rec, echo=True)
SessionLocalOrd = sessionmaker(autocommit=False, autoflush=False, bind=engine_ord)
#SessionLocalRec = sessionmaker(autocommit=False, autoflush=False, bind=engine_rec)


def get_db_ord():
    db_ord = SessionLocalOrd()
    try:
        yield db_ord
    finally:
        db_ord.close()


# def get_db_rec():
#     db_rec = SessionLocalRec()
#     try:
#         yield db_rec
#     finally:
#         db_rec.close()
