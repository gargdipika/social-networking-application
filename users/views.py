from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EmailAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework.views import APIView
from .models import FriendRequest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.views import LogoutView


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    error_message = ""
    try:
        if request.method == 'POST':
            post_data = request.POST.copy()
            email = post_data["email"].lower()
            initial_data = {
                'username': email,
                'email' : email
            }
            for key, value in initial_data.items():
                if key not in post_data:
                    post_data[key] = value
            form = EmailAuthenticationForm(request, data=post_data)
            if form.is_valid():
                user = form.get_user()
                if request:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse("Invalid request")
            else:
                error_message = "Invalid email id or password"
        else:
            form = EmailAuthenticationForm()
    except Exception as e:
        error_message = "Invalid email id or password"
    return render(request, 'users/login.html', {'form': form, 'error_message':error_message})

def home(request):
    try:
        query = request.GET.get('q')
        results = None
        page_obj = None

        if query:
            results = User.objects.filter((Q(username__icontains=query) | Q(email__icontains=query)) & (~Q(username=request.user.username)))
        if results:
            paginator = Paginator(results, 10)  # Show 10 users per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        
        pending_friend_req = FriendRequest.objects.filter((Q(from_user__username=request.user.username) | Q(to_user__username=request.user.username)) & Q(accepted=False))
        accepted_friend_req = FriendRequest.objects.filter((Q(from_user__username=request.user.username) | Q(to_user__username=request.user.username)) & Q(accepted=True))
        pending_friend_list = []
        accepted_friend_list = []
        for friend in pending_friend_req:
            if friend.from_user.username == request.user.username:
                pending_friend_list.append(friend.to_user.username + "_touser")
            else:
                pending_friend_list.append(friend.from_user.username + "_fromuser") #for from user it should show accept or reject
        for friend in accepted_friend_req:
            if friend.from_user.username == request.user.username:
                accepted_friend_list.append(friend.to_user.username)
            else:
                accepted_friend_list.append(friend.from_user.username)

        return render(request, 'users/home.html', {'page_obj': page_obj, 'query': query, "pending_friend_list":pending_friend_list, "accepted_friend_list":accepted_friend_list })
    except Exception as e:
        return render(request, 'users/message.html',{'message': e})

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    error_message = ""
    try:
        if request.method == 'POST':
            post_data = request.POST.copy()
            email = post_data["email"].lower()
            initial_data = {
                'username': email,
                'email' : email
            }
            for key, value in initial_data.items():
                if key not in post_data:
                    post_data[key] = value
            form = RegisterForm(post_data)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user is not None:
                    # Log the user in
                    login(request, user)
                    return redirect('home')
            else:
                for field in form:
                    for error in field.errors:
                        if error == "A user with that username already exists.":
                            error_message = "A user with this email id already exists."
                        else:
                            error_message = error
                        print(f"Error in {field.label} {field.value}: {error}")
        else:
            form = RegisterForm()
    except Exception as e:
        error_message = e
    return render(request, 'users/signup.html', {'form': form, 'error_message': error_message})

class CoustmizedLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, "users/message.html",{'message': 'User not logged in'})

        print(f'User {request.user.username} is logging out.')
        return super().dispatch(request, *args, **kwargs)


class SendFriendRequestView(LoginRequiredMixin, APIView):
    def post(self, request):
        try:
            to_user_name = request.data.get('to_user_name')
            to_user = User.objects.get(username=to_user_name)
            from_user = request.user
            one_minute_ago = timezone.now() - timedelta(minutes=3)

            friend_requests_in_last_minute = FriendRequest.objects.filter(from_user__username=from_user.username, created_at__gte=one_minute_ago).count()
            if friend_requests_in_last_minute<3:
                friend_request, created = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
                if created:
                    return render(request, 'users/message.html',{'message': 'Friend request sent successfully'})
                else:
                    return render(request, 'users/message.html',{'message': 'Friend request already sent'})
            else:
                return render(request, 'users/message.html',{'message': f'{from_user.username} has exceeded the limit of 3 to send friend request'})
        except Exception as e:
            return render(request, 'users/message.html',{'message': e})

class RejectFriendRequestView(LoginRequiredMixin, APIView):
    def post(self, request):
        try:
            friend_request_username = request.data.get('friend_request_username')
            friend_request = FriendRequest.objects.filter((Q(from_user__username=friend_request_username) & Q(to_user__username=request.user.username) & Q(accepted=False)))[0]
            if friend_request:
                friend_request.delete()
                return render(request, 'users/message.html',{'message': 'Friend request deleted successfully'})
            else:
                return render(request, 'users/message.html',{'message': 'Friend request not found'})
        except IndexError:
            return render(request, 'users/message.html',{'message': "You don't have any friend request with this user"})
        except Exception as e:
            return render(request, 'users/message.html',{'message': e})

class AcceptFriendRequestView(LoginRequiredMixin, APIView):
    def post(self, request):
        try:
            friend_request_username = request.data.get('friend_request_username')
            friend_request = FriendRequest.objects.filter((Q(from_user__username=friend_request_username) & Q(to_user__username=request.user.username) & Q(accepted=False)))[0]
            if friend_request:
                friend_request.accepted=True
                friend_request.save()
                return render(request, 'users/message.html',{'message': 'Friend request accepted successfully'})
            else:
                return render(request, 'users/message.html',{'message': 'Friend request not found'})
        except IndexError:
            return render(request, 'users/message.html',{'message': "You don't have any friend request with this user"})
        except Exception as e:
            return render(request, 'users/message.html',{'message': e})

@login_required
def ShowPendingFriendRequests(request):
    try:
        user_name = request.user
        pending_request = FriendRequest.objects.filter(to_user__username=user_name.username) & FriendRequest.objects.filter(accepted=False)
        page_obj = None
        if pending_request:
            paginator = Paginator(pending_request, 10)  # Show 10 users per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'users/pending_request.html', {'page_obj': page_obj})
    except Exception as e:
        return render(request, 'users/message.html',{'message': e})

@login_required
def ShowFriends(request):
    try:
        user_name = request.user
        friends = ((FriendRequest.objects.filter(from_user__username=user_name.username)) | (FriendRequest.objects.filter(to_user__username=user_name.username))) & (FriendRequest.objects.filter(accepted=True))
        page_obj = None
        if friends:
            paginator = Paginator(friends, 10)  # Show 10 users per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'users/friends.html', {'page_obj': page_obj})
    except Exception as e:
        return render(request, 'users/message.html',{'message': e})
