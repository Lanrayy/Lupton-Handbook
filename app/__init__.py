from flask import Flask
from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)
app.config.from_object('config')

from app import views
