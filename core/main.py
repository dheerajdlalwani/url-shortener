from flask import Flask, render_template, request, redirect

from models import *

project = Flask(__name__)


@project.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        data = request.form
        long_url = data['long_url']
        short_url = 'dheeraj-twitter
        return render_template('home.html', short_url=short_url)
    else:
        return render_template('home.html')





@project.route('/<string:short_url>', methods=['GET'])
def transport(short_url):
    print(short_url)
    if short_url == "dheeraj-twitter":
        return redirect('https://twitter.com/dhirucodes')
    else:
        pass


if __name__ == "__main__":
    project.run(debug=True)
