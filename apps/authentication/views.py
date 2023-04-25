from django.shortcuts import render

from apps.authentication.forms import UserRegistrationForm
from apps.core.models import UserProfile


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            # Create the UserProfile object
            UserProfile.objects.create(user=new_user)
            return render(
                request,
                "authentication/register_done.html",
                {"new_user": new_user},
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "authentication/register.html", {"user_form": user_form})
