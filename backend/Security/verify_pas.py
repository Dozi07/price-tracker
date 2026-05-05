import bcrypt

def verify_pas(entered_password, hashed_password: str) -> str:
    return bcrypt.checkpw(entered_password.encode('utf-8'), hashed_password.encode('utf-8'))


