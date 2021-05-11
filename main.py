from flask import Flask, render_template, request, redirect, session
from core.models import *
from core.helpers import *
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

SECRET = os.getenv('SECRET')
project = Flask(__name__)
project.secret_key = SECRET


FORBIDDEN_URLS = ["user", "login", "logout", "register", "user/", "login/", "logout/", "register/", "/user", "/login", "/logout", "/register", "/user/", "/login/", "/logout/", "/register/"]

@project.context_processor
def inject_today_date():
    return {'now': datetime.now()}


@project.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        print("Debug: Post Request here.")
        data = request.form
        long_url = data['long_url']
        try:
            custom_slug = data['custom_slug']
        except:
            custom_slug = ""
        if long_url != "":
            if "kata-flask.herokuapp.com" in long_url:
                message = "Cannot shorten URLs from this domain."
                return render_template('home.html', message=message)
            else:
                print("Debug: Recieved Long URL")
                if long_url[0:7] != "http://" and long_url[0:8] != "https://":
                    print(long_url[0:7])
                    long_url = "http://" + long_url
                    print(f"Maine new URL Ye banaya {long_url}")
                if custom_slug != "":
                    if custom_slug in FORBIDDEN_URLS or "kata-flask.herokuapp.com" in custom_slug:
                        message = "Invalid custom alias."
                        return render_template('home.html', message=message)                    
                    else:
                        if check_custom_slug_availability(custom_slug):
                            short_url = custom_slug
                        else:
                            message = "Custom URL already taken."
                            return render_template('home.html', message=message)                    
                else:
                    short_url = get_short_url()
                print("Debug: Recieved Short URL")
                print(f"User sent: {long_url}")
                print(f"Short URL: {short_url}")
                print(session)
                if "user" in session:
                    print("User is logged in. Fetching user email.")
                    user_email = (session_collection.find_one({"_id": session["user"]}))["email"]
                    new_url = {
                        "user": user_email,
                        "long_url": long_url,
                        "short_url": short_url,
                        "click_count": 0
                    }
                else:
                    new_url = {
                        "long_url": long_url,
                        "short_url": short_url,
                        "click_count": 0
                    }
                url_collection.insert_one(new_url)
                return render_template('home.html', short_url=short_url, long_url=long_url)
        else:
            message = "Please enter a long url!"
            return render_template('home.html', message=message)
    else:
        return render_template('home.html')




@project.route('/user/', methods=['GET'])
def user():
    if "user" in session:
        user_email = (session_collection.find_one({"_id": session["user"]}))["email"]
        user_urls = url_collection.find({"user": user_email})
        user_urls = list(user_urls)
        print(f"Showing user page for user: {user_email}.")
        return render_template('profile.html', user_email=user_email, user_urls=user_urls)
    else:
        message = "User not logged in. Please login first."
        return render_template('login.html', message=message)




@project.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        print("POST Request mili")
        if 'user' in session:
            user_email = (session_collection.find_one({"_id": session["user"]}))["email"]
            print(f"User email in session: {user_email}")
            message = f"User - {user_email} already logged in."
            return render_template('home.html', message=message)
        else:
            data = request.form
            email = data['email']
            password = data['password']
            if email != "" and password != "":
                print(f"User Email: {email}")
                print(f"User Password: {password}")
                user = user_collection.find_one({"email": email})
                if user != None:
                    print(f"User: {email} found in database.")
                    if verify_password(user['password'], password):
                        print("Their passwords matched too.")
                        message = "Logged in Successfully."
                        print("Now doing some stuff for session.")
                        # TODO some stuff here for SESSION
                        print(f"Now setting the session cookie for the user: {email} ")
                        new_session = {
                            "_id": get_unique_session_id(),
                            "domain": "127.0.0.1",
                            "email": f"{email}",
                            "set_date": f"{datetime.now()}",
                            "expiration": f"{datetime.now()+timedelta(days=1)}"
                        }
                        session_collection.insert_one(new_session)
                        session["user"] = new_session["_id"]
                        print(f"The system generated session_id: {session['user']} for the user: {email}")
                        return render_template('home.html', message=message)
                    else:
                        message = "Incorrect Password"
                        return render_template('login.html', message=message)
                else:
                    message = "User Not Found."
                    return render_template('login.html', message=message)
            else:
                message = "Please enter email and password."
                return render_template('login.html', message=message)
    else:
        print("GET Request mili")
        if 'user' in session:
            user_email = (session_collection.find_one({"_id": session["user"]}))["email"]
            print(f"User email in session: {user_email}")
            message = f"User - {user_email} already logged in."
            return render_template('home.html', message=message)
        else:
            return render_template('login.html')



@project.route('/logout/', methods=['GET', 'POST'])
def logout():
    if 'user' in session:
        user = session["user"]
        user_email = (session_collection.find_one({"_id": session["user"]}))["email"]
        print(f"User email in session: {user_email}")
        session_collection.delete_one({"_id": f"{user}"})
        session.pop('user', None)
        message = f"User logged out successfully."
        print(f"User - {user_email} logged out.")
        return render_template('home.html', message=message)
    else:
        message = "User not logged in."
        return render_template('login.html', message=message)
        

@project.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        print("POST Request mili")
        data = request.form
        email = data['email']
        password = data['password']
        if email != "" and password != "":
            print(f"User Email: {email}")
            print(f"User Password: {password}")
            existing_user = user_collection.find_one({"email": email})
            if not existing_user:
                new_user = {
                    "_id": get_unique_user_id(),
                    "email": email,
                    "password": get_password_hash(password),
                    "authenticated":False
                }
                user_collection.insert_one(new_user)
                message = "Account Created Successfully."
                return render_template('login.html', message=message)
            else:
                message = "Account already exists."
                return render_template('register.html', message=message)

        else:
            message = "Please enter email and password."
            return render_template('register.html', message=message)

    else:
        print("GET Request mili on login page.")
        return render_template('register.html')



FORBIDDEN_URLS = ["user", "login", "logout", "register", "user/", "login/", "logout/", "register/", "/user", "/login", "/logout", "/register", "/user/", "/login/", "/logout/", "/register/"]


@project.route('/<string:short_url>/', methods=['GET'])
def transport(short_url):
    if short_url == "":
        return render_template('home.html')
    url = url_collection.find_one({"short_url": short_url})
    if url != None:
        url_collection.update_one({"short_url": short_url}, { "$inc": {"click_count": 1}})

        return redirect(url['long_url'])
    else:
        message = "Sorry, the requested URL was not found."
        return render_template('home.html', message=message)


if __name__ == "__main__":
    project.run(debug=True)