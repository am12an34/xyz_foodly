from flask import*
app = Flask(__name__)

#-------------------------
@app.route("/")
def index():
    return redirect(url_for('login'))
@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/register")
def login():
    return render_template('register.html')

#--------------------------
if __name__ == '__main__':
    app.run(debug=True)
