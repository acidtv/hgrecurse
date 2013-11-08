#!/usr/bin/python

from flask import Flask, render_template
app = Flask(__name__)

import config

import hglib
from hgrecurse import Hgrecurse

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache(50)

@app.route('/')
def index():
	repo = config.repos['Azarius']
	cachekey = 'test'
	hg = Hgrecurse(repo['path'])

	commits = cache.get(cachekey)
	if commits is None:
		commits = hg.log(limit=30, branch='default')
		cache.set(cachekey, commits)

	return render_template('index.htm', entries=commits)

if __name__ == '__main__':
	app.run(debug=True)
