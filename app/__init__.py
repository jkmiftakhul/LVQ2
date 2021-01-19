from flask import Flask


app = Flask(__name__)
app.secret_key = "rahasia loooh"
from app.module.controller import *