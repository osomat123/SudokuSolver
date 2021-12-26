from flask import Flask
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c44c48de96588fefeb3986db3af0bca8'

model = load_model('SudokuSolver/printed_digits')

from SudokuSolver import routes