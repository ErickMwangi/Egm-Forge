from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # replace with a strong key in prod

MAILCHIMP_API_KEY = '01440d0e79367f4490bdfa25a70da0e0-us5'
MAILCHIMP_SERVER_PREFIX = 'us5'
MAILCHIMP_AUDIENCE_ID = 'e44c969a2f'

@app.route('/')
def home():
    show_modal = session.pop('show_modal', False)
    return render_template('opt_in.html', success=show_modal)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    company = request.form.get('company')
    industry = request.form.get('industry')
    goal = request.form.get('project_goal')

    data = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": company,
            "LNAME": industry,
            "MMERGE3": goal  
        }
    }

    url = f"https://{MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{MAILCHIMP_AUDIENCE_ID}/members"

    response = requests.post(
        url,
        auth=("anystring", MAILCHIMP_API_KEY),
        json=data
    )

    if response.status_code in [200, 204]:
        flash("Thanks for subscribing! Check your email for confirmation.")
        session['show_modal'] = True
    else:
        flash("There was an error with your subscription. Please try again.")
        session['show_modal'] = True 

    return render_template('guide.html')

@app.route('/guide')
def guide():
    
    
    return render_template('guide.html')

if __name__ == '__main__':
    app.run(debug=True)
