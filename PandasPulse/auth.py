from jose import jwt,JWTError
SECRET_KEY = "MY_SECRET_KEY"
ALGORITHM = "HS256"
def create_access_token(email: str):

    data = {
        "sub": email
    }

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except JWTError:

        return None