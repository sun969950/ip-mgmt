# -*- coding: utf-8 -*-
"""Login middleware."""

from django.contrib.auth import authenticate

from account.accounts import Account


class LoginMiddleware(object):
    """Login middleware."""

    def process_view(self, request, view, args, kwargs):
        """process_view."""
        if getattr(view, 'login_exempt', False):
            return None

        user = authenticate(request=request)
        if user:
            request.user = user
            return None

        account = Account()
        return account.redirect_login(request)
