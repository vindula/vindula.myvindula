# coding: utf-8
from five import grok
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import Interface

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.models.funcdetails import FuncDetails
from vindula.myvindula.models.status import ModelsStatus
from vindula.myvindula.models.notification import ModelsMyvindulaNotificacao
from vindula.controlpanel.content.vindulaconfigall import VindulaConfiguration


grok.templatedir('templates')

class ModalProfileView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('modal-profile')
    
    def getDataFunc(self, username):
        return FuncDetails(username)
    
    def getStatusUser(self, username):
        status = ModelsStatus.get_last_status(username)

        if status:
            status = '"'+status.text+'"'
        else:
            status = ''
        return status
    
    def getActiveCargo(self):
        vindulaconfiguration = VindulaConfiguration(self.context, self.request)
        cargo = vindulaconfiguration.check_cargo_modais()
        return cargo
        
        