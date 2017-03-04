from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
import datetime
from .models import registration, secret

# Create your views here.
def index(request):
    return render(request, "dojoSecretsApp/index.html")

def validator(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    password2 = request.POST["password2"]

    validation = registration.objects.validator(first_name, last_name, email, password, password2)

    #If there were errors, runs through each shorthand error in errorlist (validation[1]), and then translates them to the longhand error
    #in errordict (validation[2]) and turns them into flash messages, then redirects to the homepage
    if not validation[0]:
        for error in validation[1]:
            messages.info(request, validation[2][error])
        return redirect ("/")

    request.session['id'] = validation[1]
    print request.session["id"]
    return redirect ("/success")

def login(request):
    password = request.POST["password"]
    email = request.POST["email"]

    login = registration.objects.login(email, password)

    if not login[0]:
        for error in login[1]:
            messages.info(request, login[2][error])
        return redirect ("/")
    request.session['id'] = login[1]
    print request.session["id"]
    return redirect("/success")

def success(request):
    if "id" not in request.session:
        messages.info(request, "Please log in to continue.")
        return redirect("/")

    context = {
    "selection" : registration.objects.get(id = request.session["id"]),
    "allSecrets" : secret.objects.all().order_by("-created_at")[:5],
    "now" : datetime.datetime.now()
    }
    return render(request, "dojoSecretsApp/success.html", context)

def make_secret(request):
    if "id" not in request.session:
        messages.info(request, "Please log in to continue.")
        return redirect("/")

    content = request.POST["secret"]
    creator = registration.objects.get(id = request.session["id"])
    recentSecret = registration.objects.create_secret(content, creator)
    if recentSecret == False:
        messages.error(request, "Please insert content to make a post.")
    else:
        messages.info(request, "You successfully posted a secret!")
    return redirect("/success")

def order_secret(request):
    if "id" not in request.session:
        messages.info(request, "Please log in to continue.")
        return redirect("/")

    context = {
    "selection" : registration.objects.get(id = request.session["id"]),
    "allSecrets" : secret.objects.annotate(num_likes = Count("liker")).order_by("-num_likes")
    }
    return render(request, "dojoSecretsApp/ordered.html", context)

def like(request):
    if "id" not in request.session:
        messages.info(request, "Please log in to continue.")
        return redirect("/")

    secret_object = secret.objects.get(id = request.POST['secret_id'])
    clicker = registration.objects.get(id = request.session["id"])
    secret_object.liker.add(clicker)

    #Page is a hidden field which tells which page they came from so we can reroute properly
    #We make sure we're comparing to a string because that is what the form returns
    if request.POST["page"] == "1":
        return redirect("/success")
    else:
        return redirect("/order_secret")

def delete(request):
    if "id" not in request.session:
        messages.info(request, "Please log in to continue.")
        return redirect("/")

    secret.objects.get(id = request.POST['secret_id']).delete()
    messages.info(request, "Secret deleted successfully!")

    if request.POST["page"] == "1":
        return redirect("/success")
    else:
        return redirect("/order_secret")

def update(request):
    if "id" not in request.session:
        messages.info(request, "Please log in to continue.")
        return redirect("/")

    secret.objects.filter(id = request.POST['secret_id']).update(content = request.POST["newcontent"])
    secret.objects.filter(id = request.POST['secret_id']).update(updated_at = datetime.datetime.now())

    if request.POST["page"] == "1":
        return redirect("/success")
    else:
        return redirect("/order_secret")

def logout(request):
    request.session.pop("id")
    messages.info(request, "Thank you for logging out.  Goodbye!")
    return redirect("/")
