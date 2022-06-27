from flask import Flask, make_response, render_template
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CasaDelPiss'


@app.route('/', methods=['GET'])
def index():
    res = make_response(render_template('index.html'))
    return res


if __name__ == "__main__":
    serve(app, host="localhost", port="9400")
