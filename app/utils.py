import hashlib
import base64


def generate_short_code(url: str, salt: str = "") -> str:
    """
    Generates a 7-character short code from a URL using SHA-256 and Base62 encoding.

    Args:
        url: The original URL to shorten.
        salt: An optional salt to append for collision resolution.

    Returns:
        A 7-character alphanumeric string.
    """
    data_to_hash = (url + salt).encode("utf-8")

    sha256_hash = hashlib.sha256(data_to_hash).digest()
    b64_encoded = base64.urlsafe_b64encode(sha256_hash)

    short_code = b64_encoded.decode("utf-8")[:7]

    return short_code
