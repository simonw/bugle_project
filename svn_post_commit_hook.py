#!/usr/bin/python
import os, sys, urllib

MESSAGE = "%(author)s: %(log)s http://core.fort/trac/changeset/%(r)s"

repo = sys.argv[1]
revision = sys.argv[2]

author = os.popen(
    '/usr/bin/svnlook author %s -r %s' % (repo, revision)
).read().strip()
log = os.popen(
    '/usr/bin/svnlook log %s -r %s' % (repo, revision)
).read().strip()

message = MESSAGE % {
    'author': author,
    'log': log,
    'r': revision,
}
urllib.urlopen('http://bugle.fort/post/api/', urllib.urlencode({
    'username': 'subversion',
    'password': 'subversion',
    'message': message,
    'short': '%s: r%s' % (author, revision),
})).read()

sys.exit(0)
