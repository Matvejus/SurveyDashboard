from django.contrib.auth.models import Group, Permission

GROUPS_PERMISSIONS = {
    'Collaborator': [
        'view_answer',
        'view_question',
        'view_survey',
        'add_useranswer',
        'view_useranswer',
        'view_collaborationnetwork',
        'view_orgprofile',
        'change_customuser',
        'delete_customuser',
        'view_customuser',
    ],

    'Orchestrator': [
    'add_answer',
    'change_answer',
    'delete_answer',
    'view_answer',
    'add_question',
    'change_question',
    'view_question',
    'view_survey',
    'change_survey',
    'add_useranswer',
    'view_useranswer',
    'view_collaborationnetwork',
    'view_orgprofile',
    'change_customuser',
    'delete_customuser',
    'view_customuser',
    ],

    'Supervisor': [
    'add_answer',
    'change_answer',
    'delete_answer',
    'view_answer',
    'add_question',
    'change_question',
    'delete_question',
    'view_question',
    'add_survey',
    'change_survey',
    'delete_survey',
    'view_survey',
    'add_useranswer',
    'view_useranswer',
    'add_collaborationnetwork',
    'change_collaborationnetwork',
    'delete_collaborationnetwork',
    'view_collaborationnetwork',
    'add_orgprofile',
    'change_orgprofile',
    'delete_orgprofile',
    'view_orgprofile',
    'change_customuser',
    'delete_customuser',
    'view_customuser',
]
,
}

def create_group_permissions(name, permission_codenames):
    group, created = Group.objects.get_or_create(name=name)
    permissions = Permission.objects.filter(codename__in=permission_codenames)
    group.permissions.set(permissions)
    return group

def setup_groups_permissions(user, default_group='Collaborator'):
    for group_name, permission_codenames in GROUPS_PERMISSIONS.items():
        group = create_group_permissions(group_name, permission_codenames)
        if group_name == default_group:
            user.groups.add(group)

    return user
