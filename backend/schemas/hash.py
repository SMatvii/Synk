from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def get_password_hash(password):
    return PWD_CONTEXT.hash(password)