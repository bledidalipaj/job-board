from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


from .forms import SignInForm, SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/signin/")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)

        if form.is_valid():
            # authenticate and login user
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            next_page = request.POST.get("next")

            user = User.objects.filter(email=email).first()
            if user:
                authenticated_user = authenticate(
                    username=user.username, password=password
                )
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect("list_jobs")

            if not user or not authenticated_user:
                messages.warning(request, "Incorrect email or password.")
    else:
        form = SignInForm()

    return render(request, "accounts/signin.html", {"form": form})
