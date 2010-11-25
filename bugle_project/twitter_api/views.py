from bugle.models import Blast
from bugle.search import query_to_q_object
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.utils.decorators import method_decorator
from django.utils.html import escape
from twitter_api.models import TwitterProfile
import urllib

def datetime_to_twitter(dt):
    return dt.strftime('%a %b %d %H:%M:%S +0000 %Y') # Hard coded DST, ha

def dict_to_xml(dictionary, recursion=False):
    """
    Tweetdeck chokes on ElementTree's XML.
    """
    s = ''
    if not recursion:
        s += '<?xml version="1.0" encoding="UTF-8"?>'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            formatted_value = dict_to_xml(value, recursion=True)
        elif isinstance(value, list):
            formatted_value = ''.join(dict_to_xml(d, recursion=True) for d in value)
        elif value is None:
            formatted_value = ''
        elif isinstance(value, basestring):
            formatted_value = escape(value)
        else:
            formatted_value = escape(simplejson.dumps(value))
        s += '<%s>%s</%s>' % (key, formatted_value, key)
    return s

class View(object):
    resource_name = None
    login_required = False
    current_site = Site.objects.get_current() # this isn't going to change
    
    def __call__(self, request, *args, **kwargs):
        method = getattr(self, 'render_%s' % kwargs['format'], None)
        del kwargs['format']
        if method is None:
            raise Http404
        if self.login_required:
            method = login_required(method)
        return method(request, *args, **kwargs)
    
    def render_json(self, request, *args, **kwargs):
        content = simplejson.dumps(
            self.get_resource(request, *args, **kwargs),
            indent=2, cls=json.DjangoJSONEncoder, ensure_ascii=False)
        if 'callback' in request.GET:
            content = '%s(%s)' % (request.GET['callback'], content)
        return HttpResponse(content, content_type='application/json')
    
    def render_xml(self, request, *args, **kwargs):
        return HttpResponse(dict_to_xml({
            self.resource_name: self.get_resource(request, *args, **kwargs)
        }), content_type='text/xml')
    
    def get_resource(self, request, *args, **kwargs):
        raise NotImplementedError
    
    def get_user(self, request, *args, **kwargs):
        if 'user_id' in request.GET:
            return User.objects.get(id=request.GET['user_id'])
        elif 'screen_name' in request.GET:
            return User.objects.get(username=request.GET['screen_name'])
        elif 'id' in request.GET:
            try:
                user_id = int(request.GET['id'])
            except ValueError:
                return User.objects.get(username=request.GET['id'])
            else:
                return User.objects.get(id=user_id)
    
    def tweeterise_timeline(self, request, blasts):
        """
        Converts an iterable of blasts into tweets.
        """
        tweets = []
        for blast in blasts:
            tweets.append(self.tweeterise_blast(request, blast))
        return tweets
    
    def get_text(self, blast):
        text = [blast.message]
        if blast.extended:
            text.append('http://%s/blast/%s/' % (
                self.current_site.domain, 
                blast.id
            ))
        if blast.attachment:
            text.append('[ http://%s%s ]' % (
                self.current_site.domain, 
                blast.attachment.url
            ))
        return ' '.join(text)
        
    def tweeterise_blast(self, request, blast):
        d = {
            'contributors': None,
            'geo': None,
            'in_reply_to_status_id': None,
            'in_reply_to_user_id': None,
            'favorited': request.user.is_authenticated() and blast in request.user.favourites.all(),
            'source': 'Fort',
            'created_at': datetime_to_twitter(blast.created),
            'coordinates': None,
            'user': self.tweeterise_user(request, blast.user),
            'place': None,
            'id': blast.id,
            'contributors': None,
            'in_reply_to_screen_name': None,
            'truncated': False,
            'text': self.get_text(blast),
        }

        if blast.in_reply_to:
            d['in_reply_to_status_id'] = blast.in_reply_to.pk

        return d

    def get_profile_image(self, user):
        profile_image = ''
        if user.username != 'subversion':
            try:
                profile_image = 'http://' + self.current_site.domain + user.twitter_profile.profile_image.url
            except TwitterProfile.DoesNotExist:
                pass
        return profile_image

        
    def tweeterise_user(self, request, user):
        user_count = User.objects.count()
        return {
            'profile_sidebar_fill_color': 'ffffff',
            'description': '',
            'location': 'Fort.',
            'notifications': False,
            'profile_background_tile': False,
            'profile_image_url': self.get_profile_image(user),
            'statuses_count': user.blasts.count(),
            'profile_sidebar_border_color': 'eeeeee',
            'profile_use_background_image': True,
            'followers_count': user_count,
            'screen_name': user.username,
            'contributors_enabled': False,
            'lang': 'en',
            'created_at': datetime_to_twitter(user.date_joined),
            'friends_count': user_count,
            'geo_enabled': False,
            'profile_background_color': 'B2DFDA',
            'favourites_count': user.favourites.count(),
            'following': True,
            'verified': True,
            'profile_text_color': '333333',
            'protected': False,
            'time_zone': 'London',
            'name': user.get_full_name(),
            'profile_link_color': '93A644',
            'url': 'http://%s/%s/' % (self.current_site.domain, user.username),
            'id': user.id,
            'profile_background_image_url': '',
            'utc_offset': 0,
        }
    

class TimelineView(View):
    def get_blasts(self, request, *args, **kwargs):
        blasts = Blast.objects.exclude(user__username='subversion')
        if 'since_id' in request.GET:
            blasts = blasts.filter(id__gt=request.GET['since_id'])
        if 'max_id' in request.GET:
            blasts = blasts.filter(id__lte=request.GET['max_id'])
        return blasts
    
    def get_page(self, request, *args, **kwargs):
        count = 20
        try:
            count = int(request.GET['count'])
        except (ValueError, KeyError):
            pass
        try:
            count = int(request.GET['rpp'])
        except (ValueError, KeyError):
            pass
        page = 1
        try:
            page = int(request.GET['page'])
        except (ValueError, KeyError):
            pass
        try:
            return Paginator(self.get_blasts(request, *args, **kwargs).order_by('-created'), count).page(page)
        except EmptyPage:
            raise Http404
    
    def get_resource(self, request, *args, **kwargs):
        return self.tweeterise_timeline(request, self.get_page(request, *args, **kwargs).object_list)
    
    def render_xml(self, request, *args, **kwargs):
        d = {'statuses': []}
        for tweet in self.get_resource(request, *args, **kwargs):
            d['statuses'].append({'status': tweet})
        return HttpResponse(dict_to_xml({
            self.resource_name: d
        }), content_type='text/xml')


class LoginRequiredTimelineView(TimelineView):
    login_required = True


class UserTimelineView(TimelineView):
    def get_blasts(self, request):
        user = self.get_user(request)
        if not user:
            raise Http404
        return super(UserTimelineView, self).get_blasts(request).filter(
            user=user)


class MentionsView(TimelineView):
    login_required = True
    
    def get_blasts(self, request):
        return super(MentionsView, self).get_blasts(request).filter(
            mentioned_users=request.user)


class FavoritesView(TimelineView):
    login_required = True
    
    def get_blasts(self, request, id=None):
        if id:
            try:
                user_id = int(id)
            except ValueError:
                user = User.objects.get(username=id)
            else:
                user = User.objects.get(id=user_id)
        else:
            user = request.user
        return super(FavoritesView, self).get_blasts(request).filter(
            favourited_by=user)


class SearchView(TimelineView):
    def get_blasts(self, request):
        blasts = super(SearchView, self).get_blasts(request)
        if 'q' in request.GET and request.GET['q']:
            blasts = blasts.filter(query_to_q_object(request.GET['q'], 'message'))
        return blasts
    
    def get_resource(self, request):
        page = self.get_page(request)
        tweets = []
        for blast in page.object_list:
            d = {
                'text': self.get_text(blast),
                'to_user_id': None,
                'to_user': None,
                'from_user': blast.user.username,
                'metadata': {},
                'id': blast.id,
                'from_user_id': blast.user.id,
                'iso_language_code': 'en',
                'source': 'Fort',
                'profile_image_url': self.get_profile_image(blast.user),
                'created_at': datetime_to_twitter(blast.created),
            }
            if blast.in_reply_to:
                d['to_user_id'] = blast.in_reply_to.user.id
                d['to_user'] = blast.in_reply_to.user.username
            tweets.append(d)
        next_page_dict = request.GET.copy()
        next_page_dict['page'] = page.number + 1
        d = {
            'results': tweets,
            'since_id': None,
            'max_id': None, # not supported
            'refresh_url': '?' + request.GET.urlencode(),
            'results_per_page': None,
            'next_page': '?' + next_page_dict.urlencode(),
            'completed_in': 0,
            'page': page.number,
            'query': urllib.quote(request.GET.get('q', '')),
        }
        try:
            d['since_id'] = int(request.GET['since_id'])
        except (KeyError, ValueError):
            pass
        try:
            d['results_per_page'] = int(request.GET['rpp'])
        except (KeyError, ValueError):
            pass
        return d


class StatusUpdateView(View):
    login_required = True
    resource_name = 'status'
    
    def get_resource(self, request):
        if request.method != 'POST':
            raise Http404
        return self.tweeterise_blast(request, Blast.objects.create(
            user=request.user,
            message=request.POST['status'].strip(),
        ))


class FavoritesCreateView(View):
    login_required = True
    resource_name = 'status'
    
    def get_resource(self, request, id):
        blast = get_object_or_404(Blast, id=id)
        blast.favourited_by.add(request.user)
        return self.tweeterise_blast(request, blast)


class FavoritesDestroyView(View):
    login_required = True
    resource_name = 'status'
    
    def get_resource(self, request, id):
        blast = get_object_or_404(Blast, id=id)
        blast.favourited_by.remove(request.user)
        return self.tweeterise_blast(request, blast)


class UsersShowView(View):
    resource_name = 'user'
    
    def get_resource(self, request):
        user = self.get_user(request)
        if not user:
            raise Http404
        return self.tweeterise_user(request, user)
    

class VerifyCredentialsView(UsersShowView):
    login_required = True
    
    def get_resource(self, request):
        user = self.get_user(request)
        if not user:
            user = request.user
        return self.tweeterise_user(request, user)


def oauth_access_token(request):
    user = get_object_or_404(User, username=request.POST['x_auth_username'])
    return HttpResponse('oauth_token=%(user_id)s&oauth_token_secret=%(user_id)s&user_id=%(user_id)s&screen_name=%(username)s&x_auth_expires=0' % {
        'user_id': user.id,
        'username': user.username,
    })

class RateLimitStatusView(View):
    resource_name = 'hash'
    
    def get_resource(self, request):
        return {
            'remaining-hits': 9999999,
        }


class CurrentTrendsView(View):
    def get_resource(self, request):
        return {
            'trends': {
                '2010-06-22 17:20:00': [
                    {
                        'name': 'Bacon',
                        'query': 'Bacon'
                    },
                    {
                        'name': 'Space',
                        'query': 'Space'
                    },
                    {
                        'name': 'Bunnies',
                        'query': 'Bunnies'
                    },
                    {
                        'name': 'Wookie',
                        'query': 'Wookie'
                    }
                ]
            },
            'as_of': 1277227101
        }

