from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home

class CustomPortalDashboard(http.Controller):

    @http.route('/my-portal', type='http', auth='user', website=True)
    def portal_dashboard(self, **kw):
        """ Custom Portal Dashboard """
        return request.render('portal_login_redirect.portal_dashboard_template')

class PortalRedirect(Home):

    def _login_redirect(self, uid, redirect=None):
        """Redirect portal users to /my and employees to backend."""
        user = request.env['res.users'].sudo().browse(uid)

        # Internal backend users → go to web backend
        if user.has_group("base.group_user"):
            return super()._login_redirect(uid, redirect)

        # Portal users → go to portal dashboard (/my)
        if user.has_group("base.group_portal"):
            return "/my-portal"

        # Default behavior for other cases
        return super()._login_redirect(uid, redirect)
