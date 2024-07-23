from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = '2003253'
def block_common_passwords(password):
    with open('passwords.txt', 'r') as file:
        common_passwords = file.read().splitlines()

    if password in common_passwords:
        return False
    return True

def verify_password(password):

    # Check password length
    if len(password) < 8:
        return True

    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return True

    # Check for at least one lowercase letter
    if not any(char.islower() for char in password):
        return True

    # Check for at least one digit
    if not any(char.isdigit() for char in password):
        return True

    # Check for at least one special character
    special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"
    if not any(char in special_characters for char in password):
        return True
    print("passed owasp")
    return False

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('password', None)  # remove the password from the session
        return redirect('/')  # redirect to the home page
    # handle GET request here
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    password = request.form['psw']  # changed from 'password' to 'psw'
    if verify_password(password) and block_common_passwords(password):
        return redirect('/')

    session['password'] = password
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    password = session.get('password', 'Unknown')
    return render_template('welcome.html', password=password)


if __name__ == "__main__":
    app.run(debug=True)

