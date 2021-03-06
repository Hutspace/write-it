# coding=utf-8
from global_test_case import GlobalTestCase as TestCase
from subdomains.tests import SubdomainTestMixin
from ..models import Message, WriteItInstance, \
                            Moderation, Confirmation, \
                            OutboundMessage
from popit.models import Person
import datetime

class MessageDetailView(TestCase, SubdomainTestMixin):
    def setUp(self):
        super(MessageDetailView,self).setUp()
        self.writeitinstance1 = WriteItInstance.objects.all()[0]
        self.person1 = Person.objects.all()[0]
        self.message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Subject 1', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])
        Confirmation.objects.create(message=self.message, confirmated_at = datetime.datetime.now())

    def test_get_message_detail_page(self):
        #I'm kind of feeling like I need 
        #something like rspec or cucumber
        host = self.get_host_for_subdomain(self.message.writeitinstance.slug)
        url = self.message.get_absolute_url()
        self.assertTrue(url)

        response = self.client.get(url,HTTP_HOST=host)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['message'], self.message)

    def test_get_message_detail_that_was_created_using_the_api(self):
        message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Subject 1', 
            public=True,
            writeitinstance= self.writeitinstance1, 
            confirmated = True,
            persons = [self.person1])

        #this message is confirmated but has no confirmation object
        #this occurs when creating a message throu the API
        url = message.get_absolute_url()
        host = self.get_host_for_subdomain(self.message.writeitinstance.slug)
        response = self.client.get(url,HTTP_HOST=host)
        self.assertEquals(response.status_code, 200)

    def test_get_messages_without_confirmation_and_not_confirmed(self):
        message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Subject 1', 
            public=False,
            writeitinstance= self.writeitinstance1, 
            confirmated = False,
            persons = [self.person1])

        #this message is confirmated but has no confirmation object
        #this occurs when creating a message throu the API
        host = self.get_host_for_subdomain(message.writeitinstance.slug)
        url = message.get_absolute_url()
        response = self.client.get(url,HTTP_HOST=host)
        self.assertEquals(response.status_code, 404)