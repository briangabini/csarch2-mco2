# tests/__init__.py

import sys
import os

from .main_test import TestBinary128Converter

__all__ = ['TestBinary128Converter']

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))