from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EventParticipant(models.Model):
    _name = 'event.participant'
    _description = 'Event Participant'
    _order = 'name asc'

    name = fields.Char(
        string='Full Name',
        required=True
    )

    registration_ids = fields.One2many(
        'event.registration',
        'participant_id',
        string='Registrations'
    )

    email = fields.Char(
        string='Email',
        required=True
    )

    phone = fields.Char(
        string='Phone Number',
        required=True
    )

    date_of_birth = fields.Date(
        string='Date of Birth'
    )

    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other')
        ],
        string='Gender'
    )

    company = fields.Char(
        string='Company / Organization'
    )

    job_title = fields.Char(
        string='Job Title'
    )

    notes = fields.Text(
        string='Notes'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    _sql_constraints = [
        (
            'unique_participant_email',
            'unique(email)',
            'A participant with this email already exists.'
        ),
    ]

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if record.name and len(record.name.strip()) < 2:
                raise ValidationError(
                    'Participant name must contain at least 2 characters.'
                )

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError(
                    'Please enter a valid email address.'
                )

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone:
                phone = record.phone.replace(' ', '').replace('-', '').replace('+', '')
                if not phone.isdigit() or len(phone) < 10:
                    raise ValidationError(
                        'Please enter a valid phone number.'
                    )

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.today():
                raise ValidationError(
                    'Date of birth cannot be in the future.'
                )