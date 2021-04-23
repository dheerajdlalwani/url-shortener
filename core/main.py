from flask import Flask, render_template, request, redirect

project = Flask(__name__)


@project.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    project.run(debug=True)
