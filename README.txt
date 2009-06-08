bugle
=====

Group status updates for hackers in forts.

Dependencies:

- Django 1.1 beta (or later)
- Several hackers
- No internet connection
- A fort

Bugle is a Twitter-like application for groups of hackers collaborating in a 
castle (or fort, or other defensive structure) with no internet connection.
Bugle combines Twitter-style status updates with a pastebin and a group todo
list. It also has a rudimentary API automated scripts (such as the included 
subversion post-commit hook) to post messages in an unobtrusive way.

It was built as a side project during a /dev/fort week in a Scottish castle. 
See http://devfort.com/ for more details.

Server-side code is by Simon Willison, and the parts of the CSS that don't 
suck are by Natalie Downe (Simon's butchered it a bit since then).

Bugle isn't secure (vulnerable to CSRF) and probably doesn't scale.
