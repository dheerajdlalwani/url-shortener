from flask import Flask, render_template, request, redirect
from core.models import *
from core.helpers import *



project = Flask(__name__)


@project.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        print("Debug: Post Request here.")
        data = request.form
        long_url = data['long_url']
        if long_url != "":
            print("Debug: Recieved Long URL")
            if long_url[0:7] != "http://" and long_url[0:8] != "https://":
                print(long_url[0:7])
                long_url = "http://" + long_url
                print(f"Maine new URL Ye banaya {long_url}")
            short_url = get_short_url()
            print("Debug: Recieved Short URL")
            print(f"User sent: {long_url}")
            print(f"Short URL: {short_url}")
            new_url = {
                "long_url": long_url,
                "short_url": short_url,
                "click_count": 0
            }
            collection.insert_one(new_url)
            return render_template('home.html', short_url=short_url, long_url=long_url)
        else:
            message = "Please enter a long url!"
            return render_template('home.html', message=message)
    else:
        return render_template('home.html')


@project.route('/<string:short_url>', methods=['GET'])
def transport(short_url):
    if short_url == "":
        return render_template('home.html')
    url = collection.find_one({"short_url": short_url})
    if url != None:
        collection.update_one({"short_url": short_url}, {
                              "$inc": {"click_count": 1}})
        return redirect(url['long_url'])
    else:
        message = "Sorry, the requested URL was not found."
        return render_template('home.html', message=message)


if __name__ == "__main__":
    project.run(debug=True)