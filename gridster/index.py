from flask import Flask, render_template
from utils.utils import chunks

app = Flask(__name__)

@app.route("/")
def dashboard():
	c = [1,2,3,4]
	r = [1,2,3,4]
	return render_template('dashboard.html', c=c, r=r)

if __name__ == '__main__':
	app.run(debug=True)
