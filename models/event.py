from odoo import models, fields,api
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _name = 'event.event'
    _description = 'Event'
    _order = 'date desc'

    name = fields.Char(
        string='Event Name',
        required=True
    )

    event_id = fields.Char(
        string='Event ID',
        readonly=True,
        copy=False,
        default='New'
    )

    date = fields.Datetime(
        string='Event Date',
        required=True
    )

    location = fields.Char(
        string='Location'
    )

    capacity = fields.Integer(
        string='Capacity',
        required=True,
        default=0
    )

    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True
    )

    venue_id = fields.Many2one(
        'event.venue',
        string='Venue',
        ondelete='restrict'
    )

    def action_confirm(self):
        self.write({'status': 'confirmed'})

    def action_start(self):
        self.write({'status': 'ongoing'})

    def action_complete(self):
        self.write({'status': 'completed'})

    def action_cancel(self):
        self.write({'status': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'status': 'draft'})

    
    @api.constrains('capacity', 'venue_id')
    def _check_capacity(self):
        for event in self:
            if event.capacity <= 0:
                raise ValidationError(
                    "Event capacity must be greater than 0."
                )

            if event.venue_id and event.capacity > event.venue_id.capacity:
                raise ValidationError(
                    "Event capacity cannot be greater than the venue capacity."
                )
    @api.onchange('venue_id')
    def _onchange_venue_id(self):
        if self.venue_id:
            self.capacity = self.venue_id.capacity


