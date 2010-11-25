from bugle_project.bugle.models import Blast
from django.contrib.auth.models import User
from django.test import TestCase

class PostTest(TestCase):
    def test_in_reply_to(self):
        u = User(username='test')
        u.set_password('test')
        u.save()
        b1 = Blast.objects.create(
            user=u,
            message='Hello',
        )
        self.assertTrue(self.client.login(username='test', password='test'))
        res = self.client.post('/post/', {
            'message': 'Why hello there', 
            'in_reply_to': b1.pk
        })
        self.assertRedirects(res, '/')
        b2 = Blast.objects.all()[1]
        self.assertNotEqual(b1, b2)
        self.assertEqual(b1.user, u)
        self.assertEqual(b2.user, u)
        self.assertEqual(b1, b2.in_reply_to)
        

