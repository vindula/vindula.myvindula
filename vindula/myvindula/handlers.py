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


def userupdate(event):
    """ Handler for User Login in Site """
    tools = UtilMyvindula()
    
    user_login = tools.membership.getAuthenticatedMember()
    enable = tools.site.restrictedTraverse('@@myvindula-conf-userpanel').check_alert_first_access()
    
    user_id = tools.Convert_utf8(user_login.getUserName())      
        
    user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(user_id)
        
    if not user_instance or\
       not ModelsUserOpenFire().get_UserOpenFire_by_username(user_id) and\
       user_id != 'admin':
        
        if not ModelsInstanceFuncdetails().get_InstanceFuncdetails(user_id):
            id_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(user_id)
            dados = {}
            
            if user_login.getProperty('fullname'):
                dados['name'] = user_login.getProperty('fullname')
            else:
                dados['name'] = user_id
            
            dados['email'] = user_login.getProperty('email')
            
            campos = ['name','email']
            for campo in campos:
                D={}
                D['vin_myvindula_instance_id'] = id_instance
                D['vin_myvindula_confgfuncdetails_fields'] = campo
                D['valor'] = tools.Convert_utf8(dados.get(campo))
                
                ModelsDadosFuncdetails().set_DadosFuncdetails(**D)
            
            tools.setLogger('info',"Usuario criado no myvindula")
        
        if not ModelsUserOpenFire().get_UserOpenFire_by_username(user_id):
            
            CreateUserXMPP(user_id)


#        if not request.other.get('came_from') or request.other.get('came_from') == getSite().portal_url()+'/':
#            request.other["came_from"]=registro_url
#        request.response.redirect(registro_url, lock=True)

        tools.setRedirectPage('/myvindula-first-registre')
        
    else:
        user_data =  tools.get_prefs_user(user_id)
        
        if ((not user_data.get('name')) or (not user_data.get('date_birth')) or\
            (not user_data.get('phone_number')) or (not user_data.get('email'))) and enable:
            
            tools.setLogger('info',"Dados Incompletos no myvindula")
            
#            if not request.other.get('came_from') or request.other.get('came_from') == getSite().portal_url()+'/':
#                request.other["came_from"]=registro_url
#            request.response.redirect(registro_url, lock=True)


            tools.setRedirectPage('/myvindula-first-registre')

            
