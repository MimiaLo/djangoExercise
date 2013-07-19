"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse 

from polls.models import Poll

class PollMethodTest(TestCase):

	def test_was_published_recently_with_future_poll(self):
		"""
		should return False for a future date
		"""
		future_poll = Poll(pub_date=timezone.now() + datetime.timedelta(days=30))
		self.assertEqual(future_poll.was_published_recently(), False)

	def test_was_published_recently_with_old_polls(self):
		"""
		return False if the poll is older than 1 day
		"""
	 	old_poll = Poll(pub_date=timezone.now() - datetime.timedelta(days=30))
		self.assertEqual(old_poll.was_published_recently(), False)


	def test_was_published_recently_with_old_polls(self):
		"""
		return True if the date is within the last day
		"""
		recent_poll= Poll(pub_date=timezone.now() - datetime.timedelta(hours=1))
		self.assertEqual(recent_poll.was_published_recently(), True)





def create_poll(question, days):
	""" negative for polls published in the past, positive for the poll"""
	return Poll.objects.create(
		question=question, 
		pub_date=timezone.now() + datetime.timedelta(days=days)
		)

class PollViewTests(TestCase):
	def test_index_view_with_no_polls(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available.")
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_a_past_polls(self):
		create_poll(question="Past poll.", days=-30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], ['<Poll: Past poll.>']
		)

	def test_index_view_with_a_future_polls(self):
		create_poll(question="Future poll.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available.", status_code=200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])
		"""Future post should not be displayed on the index page""" 


	def test_index_view_with_a_future_and_past_polls(self):
		create_poll(question="Past poll.", days=-30)
		create_poll(question="Future poll.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], ['<Poll: Past poll.>']
		)

	def test_index_view_with_two_past_polls(self):
		create_poll(question="Past poll 1.", days=-30)
		create_poll(question="Past poll 2.", days=-5)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(
			response.context['latest_poll_list'], 
				['<Poll: Past poll 1.>', '<Poll: Past poll 2.>']
		)


class PollIndexDetailViewTest(TestCase):

	def test_detail_view_with_a_future_poll(self):
		"""Should return a 404 not found"""
		future_poll = create_poll(question='Future poll.', days=5)
		response = self.client.get(reverse('polls:detail', args=(future_poll.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll(self):
		"""Display the poll question"""
		past_poll= create_poll(question='Past poll', days=-5)
		response = self.client.get(reverse('polls:detail', args=(past_poll.id,)))
		self.assertContains(response, past_poll.question, status_code=200)



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
