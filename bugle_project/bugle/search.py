import shlex, operator
from django.db.models import Q

def query_to_q_object(query, field):
    conditions = []
    if isinstance(query, unicode):
        query = query.encode('utf8')
        # This avoids the following weird behaviour:
        # >>> shlex.split(u'simon')
        # ['s\x00i\x00m\x00o\x00n\x00']
    terms = shlex.split(query)
    for term in terms:
        negate = False
        if term.startswith('-'):
            negate = True
            term = term[1:]
        q = Q(**{'%s__icontains' % field: term})
        if negate:
            q = ~q
        conditions.append(q)
    return reduce(operator.and_, conditions)

