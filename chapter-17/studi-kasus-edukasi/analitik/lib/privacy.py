"""Anonimisasi NIM — privacy by design."""
from __future__ import annotations

import hashlib

from analitik.lib.config import INSTITUTION_SALT


def hash_nim(nim: str, salt: str = INSTITUTION_SALT) -> str:
    return hashlib.sha256(f"{salt}:{nim}".encode()).hexdigest()[:16]
