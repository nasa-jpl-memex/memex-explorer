from flask import Flask, render_template
from utils.utils import chunks
from plots import brewer, lorenz

app = Flask(__name__)

@app.route("/")
def dashboard():
	graphs = [brewer.tag, lorenz.tag]
	return render_template('dashboard.html', graphs=graphs)

if __name__ == '__main__':
	app.run(debug=True)
