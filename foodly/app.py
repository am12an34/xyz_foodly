from flask import*
app = Flask(__name__)

#-------------------------
@app.route("/")
def index():
    return "xyz"

#--------------------------
if __name__ == '__main__':
    app.run(debug=True)
