from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django import forms

import logging

# Create your views here.
from django.urls import reverse

from polls.models import Question, Choice, QuestionTest

logger = logging.getLogger(__name__)

def index(request):
    logger.debug("index!!!!")

    latest_question_list = Question.objects.all().order_by("-pub_date")[:5]

    context = {"latest_question_list": latest_question_list}

    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {"question": question})


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", context={"question": question, "error_message": "항목을 선택하지 않았습니다."})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question.id, )))


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/results.html', {"question": question})

class InputForm(forms.Form):
    name = forms.CharField(label="Your name", max_length=100)


def input(request):

    if request.method == "POST":
        form = InputForm(request.POST)

        if form.is_valid():
            new_name = form.cleaned_data["name"]

            return HttpResponseRedirect(reverse("polls:input"))
    else:
        form = InputForm()

    return render(request, "polls/input.html", {"form": form})


class ContactForm (forms.Form):
    subject = forms.CharField(label="제목", max_length=100)

    message = forms.CharField(label="내용", widget=forms.Textarea)

    sender = forms.EmailField()

    cc_myself = forms.BooleanField(required=False)

def contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data["subject"]

            logger.debug(subject)

            return HttpResponseRedirect(reverse("polls:contact"))
    else:
        form = ContactForm()

    return render(request, "polls/contact.html", {"form": form})
