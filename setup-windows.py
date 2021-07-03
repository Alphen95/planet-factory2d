from setuptools import setup
import py2exe,pygame

DATA_FILES = ["res"]

setup(
    windows=[{"script":"main.py"}],
    options={'py2exe': {'bundle_files': 1, 'compressed': True},'pygame': {'bundle_files': 1, 'compressed': True}}
)
