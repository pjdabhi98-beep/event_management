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
            'unique(participant_id)',
            'This participant is already registered.'
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

    @api.constrains('registration_date')
    def _check_registration_date(self):
        for record in self:
            if record.registration_date and record.registration_date < fields.Datetime.now():
                raise ValidationError(
                    'Registration date cannot be in the past.'
                )

    def action_confirm(self):
        for record in self:
            if record.state == 'cancelled':
                raise ValidationError(
                    'A cancelled registration cannot be confirmed.'
                )

            record.state = 'confirmed'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'