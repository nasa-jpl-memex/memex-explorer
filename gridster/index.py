from flask import Flask, render_template
from utils.utils import chunks
from plots import rbga, candlestick, colors

app = Flask(__name__)

@app.route("/")
def dashboard():
	plots = [rbga.tag, candlestick.tag, colors.tag]
	return render_template('dashboard.html', plots=plots)

if __name__ == '__main__':
	app.run(debug=True)
