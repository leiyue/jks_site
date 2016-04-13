# -*- coding: utf-8 -*-
# -*- date: 2016-04-13 14:16 -*-

def page_auth(request):
    unauthorized_page = []
    if hasattr(request, 'unauthorized_pages'):
        unauthorized_page = request.unauthorized_pages
    return {
        'unauthorized_page': unauthorized_page,
    }
