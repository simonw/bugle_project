bugle
=====

Group collaboration tools for hackers in forts.

Dependencies:

- Django 1.1 beta (or later)
- Several collaborating hackers
- A fort, castle or other defensive structure
- No internet connection

Bugle is a Twitter-like application for groups of hackers collaborating in a 
castle (or fort, or other defensive structure) with no internet connection.
Bugle combines Twitter-style status updates with a pastebin and a group todo
list. It also has a rudimentary API allowing automated scripts (such as the 
included subversion post-commit hook) to post messages in an unobtrusive way.

It was built as a side project during a /dev/fort week in a Scottish castle. 
See http://devfort.com/ for more details.

Server-side code is by Simon Willison, and the parts of the CSS that don't 
suck are by Natalie Downe (Simon's butchered it a bit since then).

Awesome/Evil Twitter API imitation by Ben Firshman.

Bugle isn't secure (vulnerable to CSRF) and probably doesn't scale.

Bugle is released under a BSD license.
