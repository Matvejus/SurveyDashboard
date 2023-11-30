from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from .forms import ContactForm
from .models import OrgProfile, CollaborationNetwork
from django.db.models import OuterRef, Exists
from users.models import CustomUser
from djf_surveys.models import UserAnswer
 

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
    fields = '__all__'
    template_name = 'new_org.html'
    success_url = '/new_collaboration'


class NewCollab(CreateView):
    model = CollaborationNetwork
    fields = "__all__"
    template_name = 'new_collaboration.html'
    success_url = '/users/register'

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

    context = {
        'user': user,
        'org': org, 
        'network': network,
        'collaborators': collaborators,
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