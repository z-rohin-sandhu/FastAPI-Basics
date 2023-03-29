from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

class Hasher:
    @staticmethod
    def get_hash(plain_text):
        return context.hash(plain_text)
    
    @staticmethod
    def verify_hash(plain_text, hashed_text):
        return context.verify(plain_text, hashed_text)
    
     