from flask import*
app = Flask(__name__)

#-------------------------
@app.route("/")
def index():
    return redirect(url_for('login'))
@app.route("/login")
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #database er kaaj korbo...
        
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('signup.html')

#--------------------------
if __name__ == '__main__':
    app.run(debug=True)
