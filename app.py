from flask import Flask, render_template, request
import random
import string
import time

app = Flask(__name__)

# Function to evaluate the strength of the password
def evaluate_password_strength(password):
    length = len(password)
    if length < 8:
        return 'Weak'
    elif 8 <= length <= 12:
        return 'Medium'
    else:
        return 'Strong'

# Function to suggest improvements based on the current password
def suggest_improvements(password):
    improvements = []
    if len(password) < 12:
        improvements.append("Increase the length of your password.")
    if not any(char.isdigit() for char in password):
        improvements.append("Include at least one number.")
    if not any(char.isupper() for char in password):
        improvements.append("Include at least one uppercase letter.")
    if not any(char.islower() for char in password):
        improvements.append("Include at least one lowercase letter.")
    if not any(char in string.punctuation for char in password):
        improvements.append("Include at least one special character.")
    return improvements

# Function to generate 5 strong passwords based on the original password
def generate_strong_passwords_from_original(original_password):
    strong_passwords = []
    
    for _ in range(5):
        password = list(original_password)
        
        if not any(char.isupper() for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.ascii_uppercase)
        if not any(char.islower() for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.ascii_lowercase)
        if not any(char.isdigit() for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.digits)
        if not any(char in string.punctuation for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.punctuation)
        
        while len(password) < 12:
            password.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
        
        random.shuffle(password)
        
        strong_passwords.append("".join(password))
    
    return strong_passwords

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_password = request.form['password']
        strength = evaluate_password_strength(original_password)
        suggestions = suggest_improvements(original_password)
        strong_passwords = generate_strong_passwords_from_original(original_password)
        
        return render_template('result.html', 
                               original_password=original_password,
                               strength=strength,
                               suggestions=suggestions,
                               strong_passwords=strong_passwords)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=555, debug=True)