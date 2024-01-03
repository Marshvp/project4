from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
import datetime
from .models import User, Posts, Following
from django.core.paginator import Paginator


def index(request):
    all_posts = Posts.objects.all().order_by("-id")
    p = Paginator(all_posts, 3)
    
    page = request.GET.get('page')
    posts = p.get_page(page)
    nums = "a" * posts.paginator.num_pages


    print(posts)
    return render(request, "network/index.html", {"posts": posts, "nums": nums})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):

    
    
    
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        
        post_content = data.get("content")


        print(post_content, user)

        post = Posts.objects.create(user=user, content=post_content)
        date = post.date.strftime('%m-%d-%Y %H:%M:%S')
        print("Hit the server")
        return JsonResponse({"message": "Post sent successfully.", 
                            "post": {
                                "content": post_content,
                                "user": user.username, 
                                "user_id": user.id,
                                "date": date
                             }
                            }, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status = 400)
    

def profile(request, user_id):

    targetUser = get_object_or_404(User, pk=user_id)
    user_posts = Posts.objects.filter(user=targetUser)
    

    print(targetUser.id)

    return render(request, "network/profile.html", {"targetUser": targetUser,
                                                    "user_posts": user_posts})



def check_following(request, targetUserId):

    targetUser = get_object_or_404(User, pk=targetUserId)

    is_following = Following.objects.filter(user_from=request.user, user_to=targetUser).exists()

    print("is following check: ", is_following)

    return JsonResponse({
                         "is_following": is_following
                         }, status=200)
 

@login_required
def follow_unfollow(request, target_user_id):
    
    if request.method == 'POST':
        # Ensure that the user is not trying to follow/unfollow themselves
        if request.user.id == target_user_id:
            return JsonResponse({"error": "Cannot follow/unfollow yourself"}, status=400)

        targetUser = get_object_or_404(User, pk=target_user_id)
        following_relation = Following.objects.filter(user_from=request.user, user_to=targetUser)

        if following_relation.exists():
            # User is already following, so unfollow
            following_relation.delete()
            action = "unfollowed"
        else:
            # User is not following, so follow
            Following.objects.create(user_from=request.user, user_to=targetUser)
            action = "followed"

        return JsonResponse({"status": f"Successfully {action} {targetUser.username}"})
    else:
        print("WHY ARE YOU GETTING")

    
@login_required
def follow_page(request):

    user = request.user

    following_users = Following.objects.filter(user_from=request.user).values_list('user_to', flat=True)

    fposts = Posts.objects.filter(user__in=following_users).order_by('-date')
    p = Paginator(fposts, 5)

    
    page = request.GET.get('page')
    posts = p.get_page(page)
    nums = "a" * posts.paginator.num_pages

    print("Following users: ", following_users)
    print("Posts: ", posts)
    return render(request, 'network/following.html', {"posts": posts, "nums": nums})


''''''