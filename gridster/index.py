from flask import Flask, render_template
from utils.utils import chunks
from plots import iris, lorenz, rbga, texas, colors, candlestick

plots = [iris, lorenz, rbga]

app = Flask(__name__)

@app.route("/")
def dashboard():
	x = [iris.a, lorenz.a, rbga.a, texas.a, colors.a, candlestick.a]
	y = [iris.b, lorenz.b, rbga.b, texas.b, colors.b, candlestick.b]
	return render_template('dashboard.html', x=x, y=y)

if __name__ == '__main__':
	app.run(debug=True)
