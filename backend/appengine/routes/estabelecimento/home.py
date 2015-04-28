# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

@login_not_required
@no_csrf
def index():
    links = [
        {
            'name': 'Twitter',
            'icon': 'fa-twitter'
        },
        {
            'name': 'Github',
            'icon': 'fa-github'
        },
        {
            'name': 'Dribbble',
            'icon': 'fa-dribbble'
        },
        {
            'name': 'Email',
            'icon': 'fa-envelope-o'
        }
    ]
    return TemplateResponse(context={'links': links})

