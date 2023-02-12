from flask import Flask, render_template, request
import requests
import smtplib
import os

app = Flask(__name__)

response = requests.get("https://api.npoint.io/0b41fc57743c3939ff60")

USERNAME = os.environ.get("USERNAME")

PASSWORD = os.environ.get("PASSWORD")
MY_EMAIL = os.environ.get("MY_EMAIL")

@app.route('/')
def home():
    all_posts = response.json()
    return render_template("index.html", posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        number = request.form['number']
        message = request.form['message']
        header = "Successfully sent message"
        print(f"{name}\n{email}\n{number}\n{message}")
        send_email(name, email, number, message)
        return render_template("contact.html", header=header)
    header = "Contact Me"
    return render_template("contact.html", header=header)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    with smtplib.SMTP("smtp@gmail.com") as connection:
        connection.starttls()
        connection.login(USERNAME, PASSWORD)
        connection.sendmail(
            from_addr=USERNAME,
            to_addrs=MY_EMAIL,
            msg=email_message)
# @app.route("/form-entry", methods=['POST'])
# def receive_data():




@app.route('/post/<int:post_id>')
def get_post(post_id):
    all_posts = response.json()
    for post in all_posts:
        if post["id"] == post_id:
            post_title = post["title"]
            post_subtitle = post["subtitle"]
            post_body = post["body"]
            post_date = post["date"]
    return render_template("post.html",
                           title=post_title,
                           subtitle=post_subtitle,
                           body=post_body,
                           date=post_date
                           )


if __name__ == "__main__":
    app.run(debug=True)