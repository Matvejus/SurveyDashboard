from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from .forms import TestSurveyForm, ContactForm
from .models import OrgProfile, TestSurvey
from django.db.models import Avg, Q, Count, F
from users.models import CustomUser
 

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

@method_decorator([login_required, group_required([ 'Orchestrator','Supervisor'])], name='dispatch')
class NewOrgView(CreateView):
    model = OrgProfile
    fields = '__all__'
    template_name = 'new_org.html'
    success_url = '/users/register'

#page of collaboraton
def orgpage(request, org_id):
    org = OrgProfile.objects.get(id = org_id)

    #survey results to put into dashboard
    survey_results = TestSurvey.objects.filter(organization_id = org_id)

    satis_stud = survey_results.filter(occupation = "STUD").aggregate(Avg('satsified'))
    satis_emp = survey_results.filter(occupation = "EMP").aggregate(Avg('satsified'))
    avg_period = survey_results.aggregate(Avg('period'))
    totalsurvs = survey_results.count()
    studs = survey_results.filter(occupation = 'STUD').count() 
    emps = survey_results.filter(occupation = 'EMP').count()

    #Radar chart queries
    stud_data = survey_results.filter(occupation='STUD').aggregate(
    avg_period=Avg('period'),
    avg_satisfaction=Avg('satsified'),
    response_count=Count('occupation'))

    emp_data = survey_results.filter(occupation='EMP').aggregate(
    avg_period=Avg('period'),
    avg_satisfaction=Avg('satsified'),
    response_count=Count('occupation'))
    
    context = {'org':org,
               'satis_stud':satis_stud,
               'satis_emp': satis_emp,
               'period':avg_period,
               'count':totalsurvs,
               'studs':studs,
               'emps':emps,
               'stud_projects': list(stud_data.values()),
               'emp_projects': list(emp_data.values()),
               }
    
    return render(request, 'organization/org_page.html', context)


def Testsurvey(request):
    if request.method != 'POST':
        form = TestSurveyForm()
    else:
        #Post data submitted, process data.
        form = TestSurveyForm(data = request.POST)
        if form.is_valid():
            new_survey = form.save(commit = False)
            new_survey.participant = request.user
            new_survey.save()
            return redirect('organization:profile')
        
    #Display form.
    context = {'form': form}
    return render(request, 'organization/survey.html', context)

def profile(request):
    user = get_object_or_404(CustomUser, id=request.user.id) 
    org = user.organization  
    network = user.collaboration_network 
    collaborators = CustomUser.objects.filter(collaboration_network=network).exclude(id=user.id)


    context = {
        'user': user,
        'org': org,
        'network': network,
        'collaborators': collaborators,
    }

    return render(request, 'organization/profile.html', context)








    
