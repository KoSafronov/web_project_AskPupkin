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



'''
TAGS = [
    {
        tag_list := ['perl', 'python', 'TechnoPark', 'MySql', 'django', 'Mail.Ru', 'Voloshin', 'Firefox'],
        "id": j,
        "title": f"Tag {j}",
        "text": F"This is all about {j}"
    } for j in tag_list
]
'''

def PageNotFound(request, exception):
    return render(request, template_name='oops', status=404)
def handler500(request, exception):
    return render(request, template_name='oops', status=500)

def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5, allow_empty_first_page=False)
    page_obj = paginator.page(page_num)
    return render(request, "index.html", {"questions": page_obj})


def hot(request):
    questions = QUESTIONS[::-1]
    page_num = request.GET.get('page', 1)
    paginator = Paginator(questions, 5, allow_empty_first_page=False)
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

def tag(request, tag_name):
    name = TAGS[tag_name]
    return render(request, "tag_page.html", {"tag": tag_name})


def oops_404(request):
    return render(request, "layouts/404_oops.html")
