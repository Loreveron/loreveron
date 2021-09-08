from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Question,Choice

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'applv/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.all()

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'applv/home.html'
    login_url = '/admin'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'applv/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'applv/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'applv/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('applv:results', args=(question.id,)))