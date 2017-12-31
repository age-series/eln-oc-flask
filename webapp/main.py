#!/usr/bin/python3

# Created by Jared Dunbar

from flask import Flask, session, redirect, url_for, escape, request, render_template, Response
import string, random, time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def generateSecureKey(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

app.secret_key = generateSecureKey(64)

if __name__ == "__main__":
    app.run()