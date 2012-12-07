 #-*- coding: utf-8 -*-
from zope.component import getUtility
from vindula.chat.interfaces import IXMPPUsers 
from Products.CMFCore.interfaces import ISiteRoot

#from vindula.myvindula.user import ModelsFuncDetails
from vindula.chat.utils.setup import CreateUserXMPP
from vindula.chat.utils.models import ModelsUserOpenFire

from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.myvindula.registration import SchemaFunc

def userupdate(event):
    """ Handler for User Login in Site """
    tools = UtilMyvindula()
   
    user_login = tools.membership.getAuthenticatedMember()
    enable = tools.site.restrictedTraverse('@@myvindula-conf-userpanel').check_alert_first_access()
    enable_chat = tools.site.restrictedTraverse('vindula-chat-config').enableConf()
    
    user_id = tools.Convert_utf8(user_login.getUserName())      
        
    user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(user_id)
        
    if enable and not user_instance:
        id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(user_id)
        dados = {}
        
        if user_login.getProperty('fullname'):
            dados['name'] = user_login.getProperty('fullname')
        else:
            dados['name'] = user_id
        
        dados['email'] = user_login.getProperty('email')
        
        campos = [u'name',u'email']
        for campo in campos:
            D={}
            D['vin_myvindula_instance_id'] = id_instance
            D['vin_myvindula_confgfuncdetails_fields'] = campo
            D['valor'] = tools.Convert_utf8(dados.get(campo))
            
            ModelsDadosFuncdetails().set_DadosFuncdetails(**D)
    
        if enable_chat and not ModelsUserOpenFire().get_UserOpenFire_by_username(user_id):
            CreateUserXMPP(user_id)
        
        tools.setLogger('info',"Usuario criado no myvindula")
        tools.setRedirectPage('/myvindula-first-registre')
    
    
    if enable_chat and not ModelsUserOpenFire().get_UserOpenFire_by_username(user_id):
        CreateUserXMPP(user_id)

        #tools.setRedirectPage('/myvindula-first-registre')
        
    else:
        user_data =  tools.get_prefs_user(user_id)
        
        if ((not user_data.get('name')) or (not user_data.get('date_birth')) or\
            (not user_data.get('phone_number')) or (not user_data.get('email'))) and enable:
            
            tools.setLogger('info',"Dados Incompletos no myvindula")
            
            tools.setRedirectPage('/myvindula-first-registre')


def onDeleteUser(event):
    user = event.object
    if user:
        return SchemaFunc().deleteUser(user)
            
