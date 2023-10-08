from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("organization:index")
    template_name = "registration/registration.html"

@login_required
def redirectgroup(request):
    user = request.user
    if user.groups.filter(name='Supervisor').exists():
        return redirect('djf_surveys:admin_survey')
    elif user.groups.filter(name='Orchestrator').exists():
        return redirect('organization:profile')
    else:
        return redirect('organization:profile')        
    
def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@method_decorator([login_required, group_required(['Collaborator', 'Orchestrator','Supervisor'])], name='dispatch')
class update_user_profile(View):
    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse('organization:profile', kwargs={'user_id': request.user.id})) # Redirect and Reverse to the profile page

    def get(self, request):
        form = CustomUserCreationForm(instance=request.user)
        return render(request, 'user_profiles/edit_profile.html', {'form': form})

