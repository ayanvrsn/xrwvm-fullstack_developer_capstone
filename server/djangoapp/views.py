import json
from functools import wraps
import requests
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import CarModel
from .restapis import get_request, post_review, analyze_review_sentiments

def api_errors(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except (ValueError, KeyError, TypeError, ValidationError):
            return JsonResponse({'error':'Invalid request'},status=400)
        except requests.RequestException:
            return JsonResponse({'error':'Backend service unavailable'},status=502)
    return wrapped

@ensure_csrf_cookie
@require_GET
def session(request):
    return JsonResponse({'userName': request.user.username if request.user.is_authenticated else None})

@require_POST
@api_errors
def login_user(request):
    data=json.loads(request.body)
    user=authenticate(request,username=data['userName'],password=data['password'])
    if user is None:
        return JsonResponse({'error':'Invalid credentials'},status=401)
    login(request,user)
    return JsonResponse({'status':'Authenticated','userName':user.username,'firstName':user.first_name,'lastName':user.last_name})

@require_POST
def logout_request(request):
    logout(request)
    return JsonResponse({'status':'Logged out'})

@require_POST
@api_errors
def registration(request):
    data=json.loads(request.body)
    name=data['userName'].strip()
    if not name or len(name)>150:
        return JsonResponse({'error':'Invalid username'},status=400)
    validate_password(data['password'])
    try:
        user=User.objects.create_user(username=name,password=data['password'],email=data.get('email',''),first_name=data.get('firstName',''),last_name=data.get('lastName',''))
    except IntegrityError:
        return JsonResponse({'error':'Username already exists'},status=409)
    login(request,user)
    return JsonResponse({'status':'Authenticated','userName':user.username},status=201)

@require_GET
@api_errors
def get_dealerships(request,state='All'):
    endpoint='fetchDealers' if state=='All' else f'fetchDealers/{state}'
    return JsonResponse({'status':200,'dealers':get_request(endpoint)})

@require_GET
@api_errors
def get_dealer_details(request,dealer_id):
    return JsonResponse({'status':200,'dealer':get_request(f'fetchDealer/{dealer_id}')})

@require_GET
@api_errors
def get_dealer_reviews(request,dealer_id):
    reviews=get_request(f'fetchReviews/dealer/{dealer_id}')
    for review in reviews:
        review['sentiment']=analyze_review_sentiments(review['review'])['sentiment']
    return JsonResponse({'status':200,'reviews':reviews})

@require_GET
def get_cars(request):
    cars=[{'CarMake':c.car_make.name,'CarModel':c.name,'CarYear':c.year} for c in CarModel.objects.select_related('car_make')]
    return JsonResponse({'CarModels':cars})

@require_POST
@api_errors
def add_review(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'Login required'},status=401)
    data=json.loads(request.body)
    if not data.get('review','').strip():
        return JsonResponse({'error':'Review cannot be empty'},status=400)
    data['name']=request.user.get_full_name() or request.user.username
    return JsonResponse({'status':200,'review':post_review(data)},status=201)
