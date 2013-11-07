#!/usr/bin/python

from flask import Flask, render_template
app = Flask(__name__)

import config

import hglib
from hgrecurse import Hgrecurse

@app.route('/')
def index():

	repo = config.repos['Azarius']

	hg = Hgrecurse(repo['path'])
	commits = hg.log(30)

	return render_template('index.htm', entries=commits)

if __name__ == '__main__':
	app.run(debug=True)
