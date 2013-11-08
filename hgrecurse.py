
import os.path
import hglib
import time

class Hgrecurse:

	repos = None

	client = None

	def __init__(self, repo):
		self.repos = [repo]
		#self.client = hglib.open(repo)
		self.repos.extend(self.get_subrepos(repo))

	#def __enter__(self):
		#return self

	#def __exit__(self, type, value, traceback):
		#self.client.close()

	def get_subrepos(self, repo):
		hgsub = os.path.join(repo, '.hgsub')
		hgsub = os.path.expanduser(hgsub)

		try:
			with open(hgsub) as f:
				subrepos = self._parse_hgsub(repo, f.read())
		except IOError as e:
			return []

		return subrepos

	def _parse_hgsub(self, repo, contents):
		lines = contents.split("\n")
		subrepos = []

		for key, value in enumerate(lines):
			subrepo = value.split(' = ')[0].strip()

			if subrepo:
				subrepos.append(os.path.join(repo, subrepo))

		return subrepos

	def log(self, limit, branch):
		entries = []

		for repo in self.repos:
			client = hglib.open(repo)
			commits = client.log(date='2013-09-03 to 2013-09-10', branch=branch)
			#commits = client.log(limit=limit)

			for commit in commits:
				entries += [{
					'repo': repo,
					'name': commit[4],
					'desc': commit[5],
					'date': commit[6],
					'dateint': time.mktime(commit[6].timetuple()),
				}]

			client.close()

		entries.sort(key=lambda commit: commit['dateint'], reverse=True)

		return entries
