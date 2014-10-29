from flask import Flask, render_template
from utils.utils import chunks
from plots import iris, lorenz, rbga

plots = [iris, lorenz, rbga]

app = Flask(__name__)

@app.route("/")
def dashboard():
	x = [iris.a, lorenz.a, rbga.a]
	y = [iris.b, lorenz.b, rbga.b]
	return render_template('dashboard.html', x=x, y=y)

if __name__ == '__main__':
	app.run(debug=True)
