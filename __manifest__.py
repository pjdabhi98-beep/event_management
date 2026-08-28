{
    'name': 'Event Management',
    'version': '1.0',
    'category': 'Events',
    'description': """
        Manage events, participants, venues and registrations.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/registration_sequence.xml',
        'views/registration_views.xml',
        'views/participant_views.xml',
    ],
    'installable': True,
    'application': True,
}