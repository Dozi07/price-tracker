from database.Creating_eng_db import SessionLocale

def get_db(): # открывает бд
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()