from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import ContactForm, NewOrgForm, NewCollaborationForm
from .models import OrgProfile, CollaborationNetwork, License
from django.db.models import OuterRef, Exists
from users.models import CustomUser
from djf_surveys.models import UserAnswer, Survey
 

# Create your views here.

def index(request):
    if request.method != 'POST':
        form = ContactForm()
    else:
        #Post data submitted, process data.
        form = ContactForm(data = request.POST)
        if form.is_valid():
            new_survey = form.save(commit = False)
            new_survey.participant = request.user
            new_survey.save()
            return redirect('organization:index')
        
    #Display form.
    context = {'form': form}
    return render(request, 'organization/landing_page.html', context)

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator


def group_required(group_names):
    def check_group(user):
        user_groups = user.groups.values_list('name', flat=True)
        return any(group_name in user_groups for group_name in group_names)

    return user_passes_test(check_group)

#@method_decorator([login_required, group_required([ 'Orchestrator','Supervisor'])], name='dispatch')
class NewOrgView(CreateView):
    model = OrgProfile
    form_class = NewOrgForm
    template_name = 'new_org.html'
    success_url = reverse_lazy('users:register')

    def form_valid(self, form):
        response = super().form_valid(form)
        license_code = form.cleaned_data['license_code']
        try:
            license_obj = License.objects.get(code=license_code)
        except License.DoesNotExist:
            form.add_error('license_code', 'Invalid license code provided.')
            return self.form_invalid(form)

        license_obj.used_for_org = True
        if license_obj.used_for_network:
            license_obj.active = False
        license_obj.save()

        self.object.license = license_obj
        self.object.save()

        return response


class NewCollab(CreateView):
    model = CollaborationNetwork
    form_class = NewCollaborationForm
    template_name = 'new_collaboration.html'
    success_url = reverse_lazy('users:register')

    def form_valid(self, form):
        response = super().form_valid(form)
        license_code = form.cleaned_data['license_code']
        try:
            license_obj = License.objects.get(code=license_code)
        except License.DoesNotExist:
            form.add_error('license_code', 'Invalid license code provided.')
            return self.form_invalid(form)

        license_obj.used_for_network = True
        if license_obj.used_for_org:
            license_obj.active = False
        license_obj.save()

        self.object.license = license_obj
        self.object.save()

        return response



import logging

logger = logging.getLogger(__name__)



#page of collaboraton
def dashboardpage(request):
    user = get_object_or_404(CustomUser, id=request.user.id) 
    org = user.organization  
    network = user.collaboration_network 


    collaborators = CustomUser.objects.filter(collaboration_network=network).exclude(id=user.id)
    # Subquery that checks if a user answer exists for each user.
    has_answer = UserAnswer.objects.filter(user=OuterRef('pk')).values('user')
    # Annotate each collaborator with whether they have an answer or not.
    collaborators = collaborators.annotate(has_answer=Exists(has_answer))

    #to return the slug of the survey of collaboration for wheel
    surveys_for_user_network = Survey.objects.filter(collaboration_network=network)

    # Accessing the slug for each survey in the filtered queryset
    survey_slugs = [survey.slug for survey in surveys_for_user_network]

    

    context = {
        'user': user,
        'org': org, 
        'network': network,
        'collaborators': collaborators,
        'survey_slug': survey_slugs[0] if survey_slugs else None,
    }
    
    return render(request, 'organization/dashboard.html', context)
    

def profile(request, user_id):
    viewed_user = get_object_or_404(CustomUser, id=user_id)  
    org = viewed_user.organization  
    network = viewed_user.collaboration_network 
    collaborators = CustomUser.objects.filter(collaboration_network=network).exclude(id=viewed_user.id)

    # Subquery that checks if a user answer exists for each user.
    has_answer = UserAnswer.objects.filter(user=OuterRef('pk')).values('user')

    # Annotate each collaborator with whether they have an answer or not.
    collaborators = collaborators.annotate(has_answer=Exists(has_answer))

    context = {
        'viewed_user': viewed_user,
        'org': org, 
        'network': network,
        'collaborators': collaborators,
    }

    return render(request, 'organization/profile_page.html', context)