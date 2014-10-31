from flask import Flask, render_template
from utils.utils import chunks
from plots import iris, lorenz, candlestick

app = Flask(__name__)

@app.route("/")
def dashboard():
	plots = [iris.tag, lorenz.tag, candlestick.tag]
	return render_template('dashboard.html', plots=plots)

if __name__ == '__main__':
	app.run(debug=True)
