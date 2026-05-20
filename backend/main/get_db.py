from database.Creating_eng_db import SessionLocale

def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()