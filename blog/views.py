from django.core.paginator import Paginator
from django.shortcuts import redirect
from .models import BlogPost, BlogUser, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm, CreateUserForm
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.contrib import messages


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
