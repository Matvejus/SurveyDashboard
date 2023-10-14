from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

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
        return redirect('organization:profile', user_id=user.id)
    else:
        return redirect('organization:profile', user_id=user.id)      
    
def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

@login_required
@group_required(['Collaborator', 'Orchestrator', 'Supervisor'])
def edit_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            update_session_auth_hash(request, user)

            return redirect(reverse('organization:profile', args=[user.id]))
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'user_profiles/edit_profile.html', {'form': form})