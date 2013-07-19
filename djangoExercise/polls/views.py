from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Poll, Choice

#def index(request):
#	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#	template = loader.get_template('polls/index.html')
#	context = RequestContext(request, {
#		'latest_poll_list': latest_poll_list,
#	})
#	output = ', '.join([p.question fro p in latest_poll_list])
#	context = {'latest_poll_list': latest_poll_list}
#	return render(request, 'polls/index.html', context)
#	return HttpResponse(template.render(context))


#def detail(request, poll_id):
#	return HttpResponse("You're lokking at the poll %s." % poll_id)
#	try:
#		poll = Poll.objects.get(pk=poll_id)
#	except Poll.DoesNotExist:
#		raise Http404

#	poll = get_object_or_404(Poll, pk=poll_id)
#	return render(request, 'polls/detail.html', {'poll': poll})


#def results(request, poll_id):
#	return HttpResponse("You're lokking at the results of poll %s." % poll_id)
#	poll = get_object_or_404(Poll, pk=poll_id)
#	return render(request, 'polls/results.html', {'poll':poll})



class IndexView(generic.ListView):
	template_name = 'polls/index.html' 
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		"""Return the last five published polls in this case"""
		return Poll.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('pub_date')[:5]
	
	#	return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/detail.html'
	
	def get_queryset(self):
		""" Exclude any polls that are not published yet"""
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'


def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):

		return render(request, 'polls/detail.html', {
				'poll':p,
				'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes +=1
		selected_choice.save()
	#Return that after a Post data, prevent from duplicate data if it goes back
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

#	return HttpResponse("You're voting at the poll %s." % poll_id)
