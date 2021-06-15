from flask import Flask, render_template

app = Flask(__name__)

from app import routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/connect')
def index():
    return render_template('connect.html')
    

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')