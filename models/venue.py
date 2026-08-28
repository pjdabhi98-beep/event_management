from odoo import models, fields,api
from odoo.exceptions import ValidationError


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
    
    @api.constrains('capacity')
    def _check_capacity(self):
        for venue in self:
            if venue.capacity <= 0:
                raise ValidationError(
                    "Venue capacity must be greater than 0."
                )



