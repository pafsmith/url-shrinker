import hashlib


def shrink_url(url):
    result = hashlib.sha256(url.encode())
    result_hex = result.hexdigest()
    truncated_hex = result_hex[:7]
    return truncated_hex
