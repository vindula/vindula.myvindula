# coding: utf-8
from five import grok
from Products.CMFCore.interfaces import ISiteRoot

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.models.recados import ModelsMyvindulaRecados

from datetime import datetime, timedelta

grok.templatedir('templates')

class MyVindulaListRecados(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindulalistrecados')

    def get_recados(self, user):
        form = self.request.form
        usernames = form.get('usernames','')
        data_inicial = form.get('data_inicial','')
        data_final = form.get('data_final','')
        subject = form.get('subject','')

        L = []

        if usernames:
            for u in usernames.split(','):
                L.append(self.Convert_utf8(u))

        if data_inicial and data_final:
            data_inicial = self.str2datetime(data_inicial) + timedelta(days=1)
            data_final = self.str2datetime(data_final)
        return ModelsMyvindulaRecados().get_myvindula_recados(receiver=user,
                                                              list_username=L,
                                                              data_inicial=data_inicial,
                                                              data_final=data_final,
                                                              subject=subject,)
    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')

    def str2datetime(self, str):
        split_date = str.split('/')
        try:
            return datetime(int(split_date[2]),
                            int(split_date[1]),
                            int(split_date[0]))
        except ValueError:
            return datetime.now()            