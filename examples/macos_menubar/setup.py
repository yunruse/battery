# call with 'py2app' in

from setuptools import setup

APP = ['menubar.py']
DATA_FILES = []
PY2APP_OPTIONS = dict(
    plist=dict(
        LSUIElement=True,
    ),
    packages=['rumps', 'battery'],
)

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': PY2APP_OPTIONS},
    setup_requires=['py2app'],
)