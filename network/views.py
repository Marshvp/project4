from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
import datetime
from .models import User, Posts


def index(request):
    all_posts = Posts.objects.all()
    
    print(all_posts)
    return render(request, "network/index.html", {"all_posts": all_posts})


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

    user_id = user_id

    return render(request, "network/profile.html", {"user_id": user_id})

''''''