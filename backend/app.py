from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

MAILCHIMP_API_KEY = '01440d0e79367f4490bdfa25a70da0e0-us5'
MAILCHIMP_SERVER_PREFIX = 'us5'  
MAILCHIMP_AUDIENCE_ID = 'e44c969a2f'

@app.route('/')
def home():
    return render_template('opt_in.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']

    data = {
        "email_address": email,
        "status": "subscribed"
    }

    url = f"https://{MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{MAILCHIMP_AUDIENCE_ID}/members"
    
    response = requests.post(
        url,
        auth=("anystring", MAILCHIMP_API_KEY),
        json=data
    )

    if response.status_code == 200 or response.status_code == 204:
        flash("Thanks for subscribing! Check your email for confirmation.")
    else:
        flash("There was an error with your subscription. Please try again.")

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
