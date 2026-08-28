from odoo import models, fields


class EventVenue(models.Model):
    _name = 'event.venue'
    _description = 'Event Venue'
    _order = 'name'

    name = fields.Char(
        string='Venue Name',
        required=True
    )

    location = fields.Char(
        string='Location',
        required=True
    )

    capacity = fields.Integer(
        string='Capacity',
        required=True,
        default=0
    )

    event_ids = fields.One2many(
        'event.event',
        'venue_id',
        string='Events'
    )

