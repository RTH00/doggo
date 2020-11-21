import secrets


def random_token(length: int) -> str:
    return secrets.token_hex(length)
