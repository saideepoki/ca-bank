from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Single shared hasher instance
_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.

    The returned value includes:
    - salt
    - parameters
    - hash
    """
    return _hasher.hash(password)

def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify a plain-text password against a stored hash.
    """
    try:
      return _hasher.verify(stored_hash, password)
    except VerifyMismatchError:
      return False
