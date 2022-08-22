from odoo import fields, models, api


class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    is_notification_service_done = fields.Boolean(string='Notification Service Done?', default=False)

    def write(self, vals):
        if 'state' in vals and vals['state'] == 'done':
            self.notification_fleet_service()
        return super(FleetVehicleLogServices, self).write(vals)

    def notification_fleet_service(self):
        template_id = self.env.ref('autoinfo_fleet.email_fleet_service_notification').id
        mail_template = self.env['mail.template'].browse(template_id)
        for fleet_service in self.filtered(lambda x: not x.is_notification_service_done):
            if fleet_service.purchaser_id.email:
                action_url = '%s/web#id=%s&view_type=form&model=fleet.vehicle.log.services' % (
                    self.get_base_url(),
                    fleet_service.id,
                )
                base_context = {
                    'data': fleet_service,
                    'action_url': action_url
                }
                email_to = fleet_service.purchaser_id.email
                email_from_usr = 'System noreply'
                email_from_mail = self.env.user.company_id.email
                email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}
                email_values = {
                    'email_from': email_from,
                    'email_to': email_to
                }
                mail_template.sudo().with_context(base_context).send_mail(fleet_service.id, force_send=True, email_values=email_values)
                fleet_service.write({'is_notification_service_done': True})
        return True
