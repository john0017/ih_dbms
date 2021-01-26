from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np


app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template("main.html")


if __name__ == '__main__':
    app.run(debug='True')
