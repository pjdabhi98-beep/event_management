from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EventRegistration(models.Model):
    _name = 'event.registration'
    _description = 'Event Registration'
    _order = 'registration_date desc'

    name = fields.Char(
        string='Registration Number',
        required=True,
        readonly=True,
        copy=False,
        default='New'
    )

    participant_id = fields.Many2one(
        'event.participant',
        string='Participant',
        required=True,
        ondelete='cascade'
    )

    event_id = fields.Many2one(
    'event.event',
    string='Event',
    required=True,
    ondelete='restrict'
)
    registration_date = fields.Datetime(
        string='Registration Date',
        default=fields.Datetime.now,
        required=True,
        readonly=True
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft',
        required=True
    )

    notes = fields.Text(
        string='Notes'
    )

    _sql_constraints = [
        (
            'unique_participant_registration',
            'unique(participant_id, event_id)',
            'This participant is already registered for this event.'
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'event.registration'
                ) or 'New'

        return super().create(vals_list)


    @api.constrains('event_id')
    def _check_event_date(self):    
        for record in self:
            if record.event_id and record.event_id.date < fields.Datetime.now():
                raise ValidationError(
                    'You cannot register for an event whose date has passed.'
                )

  

    @api.constrains('event_id', 'state')
    def _check_event_capacity(self):
        for registration in self:
            if registration.event_id and registration.state == 'confirmed':
                confirmed_count = self.search_count([
                    ('event_id', '=', registration.event_id.id),
                    ('state', '=', 'confirmed'),
                    ('id', '!=', registration.id),
                ])

                if confirmed_count >= registration.event_id.capacity:
                    raise ValidationError(
                        'Event capacity is full. This registration cannot be confirmed.'
                    )

    def action_confirm(self):
        for record in self:
            if record.state == 'cancelled':
                    raise ValidationError(
                'A cancelled registration cannot be confirmed.'
                )

            if not record.event_id:
                raise ValidationError(
                    'Please select an event before confirming the registration.'
                )

            if record.event_id.status in ['cancelled', 'completed']:
                raise ValidationError(
                    'Registration cannot be confirmed for a cancelled or completed event.'
                )

            if record.event_id.date < fields.Datetime.now():
                raise ValidationError(
                    'Registration cannot be confirmed because the event date has passed.'
                )

            record.state = 'confirmed'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'