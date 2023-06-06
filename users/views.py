from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("organization:index")
    template_name = "registration/registration.html"

def group_required(group_name):
    def check_group(user):
        group = Group.objects.get(name=group_name)
        return user.groups.filter(name=group_name).exists()

    return user_passes_test(check_group)

@method_decorator([login_required, group_required('collaborator')], name='dispatch')
class update_user_profile(View):
    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse('organization:profile'))  # Redirect and Reverse to the profile page

    def get(self, request):
        form = CustomUserCreationForm(instance=request.user)
        return render(request, 'user_profiles/edit_profile.html', {'form': form})

