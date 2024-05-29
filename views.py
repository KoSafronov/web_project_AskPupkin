import json
import math

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.views.decorators.http import require_http_methods, require_POST

from app.forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm, CorrectForm, VoteForm
from app.models import Question, Answer, Tag, Profile
from core.settings import QUESTIONS_PER_PAGE, ANSWERS_PER_PAGE


# Create your views here.
# QUESTIONS = [
#     {
#         "id": i,
#         "title": f"Question {i}",
#         "text": F"This is question number {i}"
#     } for i in range(200)
# ]


def post_list_all(request):
    posts = Post.objects.filter(is_published=True)
    limit = request.GET.get('limit', 10)
    num_page = request.GET.get('page', 1)
    paginator = Paginator(posts, limit)
    page = paginator.page(num_page)  # Page
    return render(request, 'blog/post_by_tag.html', {
        'posts': page.object_list,
        'paginator': paginator, 'page': page,
    })


#
# def PageNotFound(request, exception):
#     return render(request, template_name='oops', status='404')
#
#
# def handler500(request, exception):
#     return render(request, template_name='oops', status=500)


def paginate(items, request, *, per_page=5):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(items, per_page)

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(1)

    return page_obj


# def index(request):
#     page_num = request.GET.get('page', 1)
#     paginator = Paginator(QUESTIONS, 5, allow_empty_first_page=False)
#     page_obj = paginator.page(page_num)
#     return render(request, "index.html", {"questions": page_obj})


def index(request):
    new_questions = list(Question.objects.new_questions())
    page_obj = paginate(new_questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }
    return render(request, 'index.html', context)


# def hot(request):
#     questions = QUESTIONS[::-1]
#     page_num = request.GET.get('page', 1)
#     paginator = Paginator(questions, 5, allow_empty_first_page=False)
#     page_obj = paginator.page(page_num)
#     return render(request, "hot.html", {"questions": page_obj})


def hot_questions(request):
    questions = list(Question.objects.hot_questions())
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'hot_questions.html', context)


#
# @login_required(login_url="login")
# def login(request):
#     return render(request, "login.html")


# def log_in(request):
#     print(request.GET)
#     print(request.POST)
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)
#     if user:
#         return redirect(reverse('index'))
#     print('Failed to login')
#     return render(request, "login.html")


@require_http_methods(['GET', 'POST'])
# @csrf_protect
@requires_csrf_token
def login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                redirect_to = request.GET.get('continue', reverse('index'))
                return redirect(redirect_to)

    context = {
        'form': login_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'login.html', context)


# @require_http_methods(['GET', 'POST'])
# @csrf_protect
# def login(request):
#     login_form = LoginForm()
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user = auth.authenticate(request, **login_form.cleaned_data)
#             if user:
#                 auth.login(request, user)
#                 redirect_to = request.GET.get('continue', reverse('index'))
#                 return redirect(redirect_to)
#
#     context = {
#         'form': login_form,
#         'pop_tags': Tag.objects.get_pop_tags(),
#         'best_members': Profile.objects.get_best_profiles(),
#     }
#
#     return render(request, 'login.html', context)


# def ask(request):
#     return render(request, "ask.html")
@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def ask(request):
    ask_form = AskForm(request.user)
    if request.method == 'POST':
        ask_form = AskForm(request.user, request.POST)
        if ask_form.is_valid():
            question = ask_form.save()
            if question:
                return redirect('question', question_id=question.id)

    context = {
        'form': ask_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'ask.html', context)


def register(request):
    return render(request, "register.html")


@require_http_methods(['GET', 'POST'])
# @csrf_protect
@requires_csrf_token
def settings(request):
    context = {
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }
    return render(request, "settings.html", context)


@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', reverse('index')))


# def question(request, question_id):
#     item = QUESTIONS[question_id]
#     return render(request, "question_detail.html", {"question": item})

def question(request, question_id):
    question = Question.objects.get_question(question_id)
    answers = list(Answer.objects.get_answers(question_id))
    page_obj = paginate(answers, request, per_page=ANSWERS_PER_PAGE)

    answer_form = AnswerForm(request.user, question)

    context = {
        'form': answer_form,
        'question': question,
        'answers': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'question_details.html', context)


def tag(request, tag_name):
    name = TAGS[tag_name]
    return render(request, "tag_page.html", {"tag": tag_name})


def oops_404(request):
    return render(request, "layouts/404_oops.html")


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def answer(request, question_id):
    question = Question.objects.get_question(question_id)
    answer_form = AnswerForm(request.user, question, request.POST)
    if answer_form.is_valid():
        answer = answer_form.save()
        answers_count = Answer.objects.get_answers(question_id).count()
        return redirect(
            reverse('question', kwargs={'question_id': question_id})
            + f'?page={math.ceil(answers_count / ANSWERS_PER_PAGE)}'
            + f'#{answer.id}'
        )


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def correct(request):
    body = json.loads(request.body)

    correct_form = CorrectForm(body)
    if correct_form.is_valid():
        answer = correct_form.save()
        body['is_correct'] = answer.is_correct
        return JsonResponse(body)

    body['is_correct'] = False
    return JsonResponse(body)


@login_required(login_url='login', redirect_field_name='continue')
@require_POST
@csrf_protect
def vote(request):
    body = json.loads(request.body)

    vote_form = VoteForm(request.user, body)
    if vote_form.is_valid():
        rating = vote_form.save()
        body['rating'] = rating
        return JsonResponse(body)

    body['rating'] = 0
    return JsonResponse(body)


@csrf_protect
def signup(request):
    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))

    context = {
        'form': signup_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'signup.html', context)


@csrf_protect
def register(request):
    register_form = SignupForm()
    if request.method == 'POST':
        register_form = SignupForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('index'))

    context = {
        'form': register_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'register.html', context)


def questions_by_tag(request, tag_name):
    questions = list(Question.objects.questions_by_tag(tag_name))
    page_obj = paginate(questions, request, per_page=QUESTIONS_PER_PAGE)

    context = {
        'questions': page_obj,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
        'tag_name': tag_name,
    }

    return render(request, 'tag.html', context)
    #return render(request, 'tag_page.html', context)


@login_required(login_url='login', redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
@csrf_protect
def profile(request):
    profile_form = ProfileForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('profile'))

    context = {
        'form': profile_form,
        'pop_tags': Tag.objects.get_pop_tags(),
        'best_members': Profile.objects.get_best_profiles(),
    }

    return render(request, 'profile.html', context)
