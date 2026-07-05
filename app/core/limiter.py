"""
limiter.py - Global Rate Limiting Configuration

This file defines and exposes the global Limiter instance.
It uses the 'get_remote_address' function to identify and limit requests based on the client's IP address.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
