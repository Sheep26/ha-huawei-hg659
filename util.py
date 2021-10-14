import re
import hashlib
import base64 as b64


_WHITESPACE_RX = re.compile(r"\s")


def base64(s):
    """
    Base64 encode a string, removing all whitespace from the output.
    """
    encoded = b64.encodebytes(s.encode()).decode()
    return _WHITESPACE_RX.sub("", encoded)  # remove all whitespace


def sha256(s):
    """
    Encode a string into its SHA256 hex digest
    """
    return hashlib.sha256(s.encode()).hexdigest()
