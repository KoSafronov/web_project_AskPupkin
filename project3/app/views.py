from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title": f"Question {i}",
        "text": F"This is question number {i}"
    } for i in range(200)
]


def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page_obj = paginator.page(page_num)
    return render(request, "index.html", {"questions": page_obj})


def hot(request):
    questions = QUESTIONS[::-1]
    page_num = request.GET.get('page', 1)
    paginator = Paginator(questions, 5)
    page_obj = paginator.page(page_num)
    return render(request, "hot.html", {"questions": page_obj})


def login(request):
    return render(request, "login.html")


def ask(request):
    return render(request, "ask.html")


def settings(request):
    return render(request, "settings.html")


def register(request):
    return render(request, "register.html")

def settings(request):
    return render(request, "settings.html")

def logout(request):
    return render(request, "logout.html")

def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, "question_detail.html", {"question": item})