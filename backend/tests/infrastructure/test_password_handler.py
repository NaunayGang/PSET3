"""Tests for password handling."""

import pytest
from src.infrastructure.auth.password_handler import hash_password, verify_password


def test_hash_password():
    """Test password hashing."""
    password = "secure_password123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 0


def test_verify_correct_password():
    """Test verifying correct password."""
    password = "secure_password123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) is True


def test_verify_wrong_password():
    """Test verifying wrong password."""
    password = "secure_password123"
    hashed = hash_password(password)
    
    assert verify_password("wrong_password", hashed) is False


def test_hash_consistency():
    """Test that same password produces different hashes."""
    password = "test"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
