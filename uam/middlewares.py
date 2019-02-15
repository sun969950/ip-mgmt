# -*- coding: utf-8 -*-
from uam.client import check_login_auth_from_server, redirect_to_403


class AccessMiddleware(object):

    def process_view(self, request, view, args, kwargs):
        res, is_super_user = check_login_auth_from_server(request.user.username)
        if res:
            request.user.is_super_user = is_super_user
            return None
        else:
            return redirect_to_403()

