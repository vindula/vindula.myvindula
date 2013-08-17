# coding: utf-8
from five import grok
from Products.CMFCore.interfaces import ISiteRoot

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.models.recados import ModelsMyvindulaRecados

grok.templatedir('templates')

class MyVindulaListRecados(grok.View,UtilMyvindula):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    grok.name('myvindulalistrecados')

    def get_recados(self, user):
        return ModelsMyvindulaRecados().get_myvindula_recados(receiver=user)

    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();

        if not open_for_anonymousUser:
            pass
            # form = self.request.form
            # excluir = form.get('form.excluir', False)

            # if excluir:
            #     id_recado = int(form.get('id_recado','0'))
            #     ModelsMyvindulaRecados().del_myvindula_recados(id_recado)
            #     IStatusMessage(self.request).addStatusMessage(_(u'Registro removido com sucesso.'),"info")

        else:
            self.request.response.redirect(self.context.absolute_url() + '/login')