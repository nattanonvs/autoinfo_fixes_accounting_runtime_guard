from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    notify_deadline = fields.Boolean(string='Notify Deadline', default=True, copy=False)
    is_notify = fields.Boolean(string='Is Notify?', default=False, copy=False)

    def write(self, vals):
        if 'stage_id' in vals:
            for task in self:
                if task.stage_id.id != vals['stage_id']:
                    new_stage_id = self.env['project.task.type'].browse(vals['stage_id'])
                    if new_stage_id and new_stage_id.sequence < task.stage_id.sequence:
                        raise ValidationError('Cannot update stage backward.')
        return super(ProjectTask, self).write(vals)

    def action_send_notify_deadline_email(self):
        template_id = self.env.ref('autoinfo_project.email_project_task_notice_deadline_template').id
        mail_template = self.env['mail.template'].browse(template_id)
        project_task_ids = self.env['project.task'].search([('notify_deadline', '=', True), ('is_notify', '=', False), ('date_deadline', '<=', fields.Date.today())])
        for task in project_task_ids:
            for user in task.user_ids:
                action_url = '%s/web#id=%s&view_type=form&model=project.task' % (
                    self.get_base_url(),
                    task.id,
                )
                base_context = self._context
                base_context.update({
                    'team': user,
                    'data': task,
                    'action_url': action_url
                })
                email_to = user.work_email
                email_from_usr = 'System noreply'
                email_from_mail = self.env.user.company_id.email
                email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}
                email_values = {
                    'email_from': email_from,
                    'email_to': email_to
                }
                mail_template.sudo().with_context(base_context).send_mail(task.id, force_send=True, email_values=email_values)
            task.write({'is_notify': True})
        return True

    def project_task_deadline_notification(self):
        self.action_send_notify_deadline_email()
