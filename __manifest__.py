{
    'name': 'Event Management',
    'version': '1.0',
    'category': 'Events',
    'summary': 'Event and Venue Management',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/registration_sequence.xml',
        'views/event_views.xml',
        'views/venue_views.xml',
        'views/registration_views.xml',
        'views/participant_views.xml',
    ],
    'installable': True,
    'application': True,
}
