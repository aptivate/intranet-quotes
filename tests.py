"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.core.urlresolvers import reverse

from binder.test_utils import AptivateEnhancedTestCase
from binder.models import IntranetUser

from models import Quote

class QuotesTest(AptivateEnhancedTestCase):
    fixtures = ['test_programs', 'test_permissions', 'test_users']

    def setUp(self):
        AptivateEnhancedTestCase.setUp(self)
        self.john = IntranetUser.objects.get(username='john')
        self.ringo = IntranetUser.objects.get(username='ringo')
        self.login(self.john)

    def login(self, user=None):
        if user is None:
            user = self.ringo
        super(QuotesTest, self).login(user)

    def test_current_classmethod(self):
        self.assertIsNone(Quote.latest)
        
        from datetime import datetime, timedelta
        now = datetime.now()
        foo = Quote(quote="Foo", by="Bar", created=now, promoted=now)
        foo.save()
        self.assertEqual(foo, Quote.latest)
        
        one_second = timedelta(seconds=1)
        bonk = Quote(quote="Bonk", by="Bink", created=now,
            promoted=now + one_second)
        bonk.save()
        self.assertEqual(bonk, Quote.latest)

        one_second = timedelta(seconds=1)
        buzz = Quote(quote="Buzz", by="Baz", created=now + one_second,
            promoted=now - one_second)
        bonk.save()
        self.assertEqual(bonk, Quote.latest) # buzz.promoted < bonk.promoted
    
    def test_admin_form_promote_button(self):
        self.login()
        response = self.client.get(reverse('admin:quotes_quote_add'))
        promote_button = self.get_page_element('.//' + 
            self.xhtml('input') + '[@name="_promote"]')
        self.assertEqual('Save and Promote', promote_button.attrib['value'])
        
        form = self.extract_admin_form(response)
        params = self.update_form_values(form.form)
        params['quote'] = '42'
        params['by'] = 'Douglas Adams'
        params['_promote'] = 'Save and Promote'
        
        response = self.client.post(reverse('admin:quotes_quote_add'),
            params, follow=True)
        self.assert_changelist_not_admin_form_with_errors(response)
        
        quote = Quote.latest
        self.assertIsNotNone(quote.promoted)
        self.assertNotEqual('', quote.promoted)
