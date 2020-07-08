from django.shortcuts import redirect, render

from .forms import SignUpForm


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("/")  # TODO: redirect to login
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
