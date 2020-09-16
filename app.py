from flask import Flask, request,render_template, jsonify
from evaluator import Evaluate
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("popup.html")

@app.route('/process', methods=['POST'])
def process():
    email = request.form['email']
    name = request.form['name']
    if name and email:
        ev = Evaluate(email)
        r = ev.get_recommendations()

        return jsonify({'name':r[0]})
    return jsonify({'error':'Missing data'})
if __name__ == '__main__':
    app.run(debug=True,port=5000)