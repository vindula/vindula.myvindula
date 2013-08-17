# coding: utf-8
from five import grok
from Products.CMFCore.interfaces import ISiteRoot

from vindula.myvindula.tools.utils import UtilMyvindula

grok.templatedir('templates')

class MyVindulaProjects(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindulaprojects')

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if not open_for_anonymousUser:
            pass
        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')