from users.forms import UserRegistrationForm

def registration_form(request):
    return {
        'registration_form': UserRegistrationForm()
    }