from flask import Flask, render_template, request, flash, session
import requests
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'


MAILCHIMP_API_KEY = '01440d0e79367f4490bdfa25a70da0e0-us5'
MAILCHIMP_SERVER_PREFIX = 'us5'
MAILCHIMP_AUDIENCE_ID = 'e44c969a2f'


SENDER_EMAIL = 'rickthetri20@gmail.com'      
RECEIVER_EMAIL = 'rickthetri20@gmail.com'     
EMAIL_PASSWORD = 'rickthetri20@gmail.com'    

def send_notification_email(email, company, industry, goal):
    subject = "🚨 New Subscription Attempt"
    body = f"""
    Someone just tried to subscribe via your site:

    Email: {email}
    Company: {company}
    Industry: {industry}
    Project Goal: {goal}
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Notification email sent!")
    except Exception as e:
        print("Failed to send notification email:", e)


@app.route('/')
def home():
    show_modal = session.pop('show_modal', False)
    return render_template('index.html', success=show_modal)


@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    company = request.form.get('company')
    industry = request.form.get('industry')
    goal = request.form.get('project_goal')

    send_notification_email(email, company, industry, goal)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
