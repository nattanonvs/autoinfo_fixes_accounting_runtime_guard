from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    insurance_expire_date = fields.Date(string='Insurance Expire Date')
    act_expire_date = fields.Date(string='Act Expire Date')
    is_notification_insurance_expire_date = fields.Boolean(string='Notification Insurance Expire Date?', default=False)
    is_notification_act_expire_date = fields.Boolean(string='Notification Act Expire Date?', default=False)

    def notification_fleet_expire_date(self, is_insuarance=False, is_act=False):
        template_id = False
        if is_insuarance:
            template_id = self.env.ref('autoinfo_fleet.email_vehicle_insurance_notification').id
            self.write({'is_notification_insurance_expire_date': True})
        elif is_act:
            template_id = self.env.ref('autoinfo_fleet.email_vehicle_act_notification').id
            self.write({'is_notification_act_expire_date': True})

        if template_id:
            mail_template = self.env['mail.template'].browse(template_id)
            if self.driver_id and self.driver_id.email:
                action_url = '%s/web#id=%s&view_type=form&model=fleet.vehicle' % (
                    self.get_base_url(),
                    self.id,
                )
                base_context = {
                    'data': self,
                    'action_url': action_url
                }
                email_to = self.driver_id.email
                email_from_usr = 'System noreply'
                email_from_mail = self.env.user.company_id.email
                email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}
                email_values = {
                    'email_from': email_from,
                    'email_to': email_to
                }
                mail_template.sudo().with_context(base_context).send_mail(self.id, force_send=True, email_values=email_values)
        return True

    def fleet_expire_date_notification(self):
        alert_insurance_expired = int(self.env['ir.config_parameter'].sudo().get_param('autoinfo_fleet.alert_insurance_expired', default=30))
        fleet_insurance_expire = self.env['fleet.vehicle'].sudo().search([('insurance_expire_date', '!=', False), ('is_notification_insurance_expire_date', '=', False), ('driver_id', '!=', False), ('vehicle_type', '=', 'car')])
        fleet_act_expire = self.env['fleet.vehicle'].sudo().search([('act_expire_date', '!=', False), ('is_notification_act_expire_date', '=', False), ('driver_id', '!=', False), ('vehicle_type', '=', 'car')])
        for insurance in fleet_insurance_expire:
            if insurance.insurance_expire_date + relativedelta(days=-alert_insurance_expired) <= fields.Date.today():
                insurance.notification_fleet_expire_date(is_insuarance=True)
        for act in fleet_act_expire:
            if insurance.act_expire_date + relativedelta(days=-alert_insurance_expired) <= fields.Date.today():
                act.notification_fleet_expire_date(is_act=True)
        return True
