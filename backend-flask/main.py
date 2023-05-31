from flask import Flask, request, jsonify
from flask_cors import CORS


from models import db, setup_db


app = Flask(__name__)


if __name__ == '__main__':
    app.run()