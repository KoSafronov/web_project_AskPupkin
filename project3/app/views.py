
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "title": f"Question {i}",
        "text": F"This is question number {i}"
    } for i in range(10)
]

def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})


def hot(request):
    questions = QUESTIONS[5:]
    return render(request, "hot.html", {"questions": questions})