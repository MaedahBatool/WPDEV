# Time based snippets being storred in private repos
# but the record keeping is public for software audits
# instead of providing them access
from datetime import date, timedelta
from random import randint
from time import sleep
import sys
import subprocess
import os
import urllib


# returns a date string for the date that is N days before STARTDATE
# for cron job based run
def get_date_string(n, startdate):
	d = startdate - timedelta(days=n)
	rtn = d.strftime("%a %b %d %X %Y %z +0500")
	return rtn

# main app
def main(argv):
	if len(argv) < 1 or len(argv) > 2:
		print "Error: Bad input."
		sys.exit(1)
	n = int(argv[0])
	if len(argv) == 1:
		startdate = date.today()
	if len(argv) == 2:
		startdate = date(int(argv[1][0:4]), int(argv[1][5:7]), int(argv[1][8:10]))
	i = 0
	while i <= n:
		curdate = get_date_string(i, startdate)
		num_commits = randint(3, 5)
		for commit in range(0, num_commits):
			commitmessage = urllib.urlopen("http://whatthecommit.com/index.txt").read()
			subprocess.call("echo 'Cron job: Private Commit #"+ str(randint(0, 1000000)) +" at " + curdate +"' > trackprivatecommits.diff; git add .; GIT_AUTHOR_DATE='" + curdate + "' GIT_COMMITTER_DATE='" + curdate + "' git commit -m 'PRIVATE COMMIT: #" + str(randint(0, 1000000)) +" at " + commitmessage +"';", shell=True)
			sleep(.5)
		i += 1

	subprocess.call("git push;", shell=True)
	#subprocess.call("git rm trackprivatecommits.diff; git commit -m 'delete'; git push;", shell=True)

if __name__ == "__main__":
	main(sys.argv[1:])
