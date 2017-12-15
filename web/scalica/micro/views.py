from rpc_search.index import indexer
from rpc_search.rpc_search import rpc_search
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .models import Following, Post, FollowingForm, PostForm, MyUserCreationForm, SearchForm

# Anonymous views
#################
def index(request):
  if request.user.is_authenticated():
    return home(request)
  else:
    return anon_home(request)

def anon_home(request):
  return render(request, 'micro/public.html')

def stream(request, user_id):  
  # See if to present a 'follow' button
  form = None
  if request.user.is_authenticated() and request.user.id != int(user_id):
    try:
      f = Following.objects.get(follower_id=request.user.id,
                                followee_id=user_id)
    except Following.DoesNotExist:
      form = FollowingForm
  user = User.objects.get(pk=user_id)
  post_list = Post.objects.filter(user_id=user_id).order_by('-pub_date')
  paginator = Paginator(post_list, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1) 
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)
  context = {
    'posts' : posts,
    'stream_user' : user,
    'form' : form,
  }
  return render(request, 'micro/stream.html', context)

def search(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    form.text = request.POST['text']
    rpc_success = False
    while not rpc_success:
      try:
        results = rpc_search.search(form.text)
        rpc_success = True
      except:
        continue

    post_list = []
    user_list = []
    result_list = []
    for post_id in results:
			filtered = Post.objects.filter(id=post_id)
			post_list.append(filtered.values_list('text', flat=True))
			user_id = filtered.values_list('user_id', flat=True)
			user_list.append(User.objects.get(pk=user_id))
	
    for i in range(0, len(post_list)):
      print(user_list[i])
      print(post_list[i])
      result_list.append({'user': user_list[i], 'post': post_list[i]})

  paginator = Paginator(post_list, 10)

  page = request.GET.get('page')
  try:
    post_list = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    post_list = paginator.page(1) 
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    post_list = paginator.page(paginator.num_pages)
  context = {
    'num_results' : len(result_list),
	'results' : result_list,
    'form' : form
  }
  return render(request, 'micro/search.html', context)

# return render(request, 'micro/post.html', {'form' : form})

def register(request):
  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    new_user = form.save(commit=True)
    # Log in that user.
    user = authenticate(username=new_user.username,
                        password=form.clean_password2())
    if user is not None:
      login(request, user)
    else:
      raise Exception
    return home(request)
  else:
    form = MyUserCreationForm
  return render(request, 'micro/register.html', {'form' : form})

# Authenticated views
#####################
@login_required
def home(request):
  '''List of recent posts by people I follow'''
  try:
    my_post = Post.objects.filter(user=request.user).order_by('-pub_date')[0]
  except IndexError:
    my_post = None
  follows = [o.followee_id for o in Following.objects.filter(
    follower_id=request.user.id)]
  post_list = Post.objects.filter(
      user_id__in=follows).order_by('-pub_date')[0:10]
  context = {
    'post_list': post_list,
    'my_post' : my_post,
    'post_form' : PostForm,
    'search_form' : SearchForm
  }
  return render(request, 'micro/home.html', context)

# Allows to post something and shows my most recent posts.
@login_required
def post(request):
  if request.method == 'POST' and request.POST.get("text"):
    form = PostForm(request.POST)
    new_post = form.save(commit=False)
    new_post.user = request.user
    new_post.pub_date = timezone.now()
    new_post.save()
    rpc_success = False
    while not rpc_success:
      try:
        indexer.index_post(new_post.id, new_post.text)
        rpc_success = True
      except:
        continue
    return home(request)
  else:
    form = PostForm
  return home(request)
  #return render(request, 'micro/post.html', {'form' : form})

@login_required
def follow(request):
  if request.method == 'POST':
    form = FollowingForm(request.POST)
    new_follow = form.save(commit=False)
    new_follow.follower = request.user
    new_follow.follow_date = timezone.now()
    new_follow.save()
    return home(request)
  else:
    form = FollowingForm
  return render(request, 'micro/follow.html', {'form' : form})
