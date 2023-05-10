from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import BlogPost, BlogUser, Comment
from .forms import BlogPostForm, CreateUserForm, ContactUsForm
from .tasks import send_mail as celery_send_mail


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user)
            return redirect('blog:login')

    contex = {'form': form}
    return render(request, 'blog/register.html', contex)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('blog:home')
        else:
            messages.info(request, 'Username or Password is incorrect')
    contex = {}
    return render(request, 'blog/login.html', contex)


def logoutUser(request):
    logout(request)
    return redirect('blog:login')


@login_required(login_url='blog:login')
def profile(request):
    user = request.user
    if request.method == 'POST':
        user.bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')
        if avatar:
            user.avatar = avatar
        user.save()
        return redirect('blog:home')
    return render(request, 'blog/profile.html', {'user': user})


def home(request):
    users = BlogUser.objects.all()
    contex = {'users': users}
    return render(request, 'blog/home.html', contex)


def post_list(request):
    posts = BlogPost.objects.filter(is_published=True).prefetch_related(Prefetch('author', queryset=BlogUser.objects.only('username')))
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


@login_required(login_url='blog:login')
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})


def delete_blog_post(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    post.delete()
    return redirect('blog:post_list')


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id, is_published=True)
    comments = post.comments.filter(is_published=True)
    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'blog/detail.html', context)


def add_comment(request, post_id):
    post = BlogPost.objects.get(pk=post_id)

    if request.method == 'POST':
        text = request.POST['text']

        comment = Comment(blogpost=post, text=text)
        comment.save()

        return redirect('blog:post_detail', post_id=post_id)

    return redirect('blog:post_detail', post_id=post_id)


def contact_us(request):
    data = dict()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            data['form_is_valid'] = True
            customer_name = form.cleaned_data['name']
            customer_email = form.cleaned_data['email']
            subj = form.cleaned_data['subject']
            mes = form.cleaned_data['text']
            subject = 'New user application!'
            message = f'Name: {customer_name}\nEmail: {customer_email}\nSubject: {subj}\nMessage: {mes}'
            celery_send_mail.apply_async((subject, message, settings.NOREPLY_EMAIL, (settings.CONTACT_EMAIL, )))
        else:
            data['form_is_valid'] = False
    else:
        form = ContactUsForm()
    data['html_form'] = render_to_string('blog/contact_us.html', {'form': form}, request=request)
    return JsonResponse(data)
