 #-*- coding: utf-8 -*-

# from vindula.chat.interfaces import IXMPPUsers
# from vindula.chat.utils.setup import CreateUserXMPP
# from vindula.chat.utils.models import ModelsUserOpenFire


from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails

from vindula.myvindula.tools.utils import UtilMyvindula

#TODO: Limpar imports e codigo velho
def userupdate(event):
    """ Handler for User Login in Site """
    tools = UtilMyvindula()
    user_login = tools.membership.getAuthenticatedMember()
    alert_first_access = tools.site.restrictedTraverse('@@myvindula-conf-userpanel').check_alert_first_access()

    # enable_chat = tools.site.restrictedTraverse('vindula-chat-config').enableConf()
    user_schema = ModelsDadosFuncdetails()
    user_id = tools.Convert_utf8(user_login.getUserName())

    #Procurando perfil do usuario
    user_instance = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstance(user_id)

    #Se nao tiver perfil, cria o perfil
    if alert_first_access and not user_instance:

        dados = {u'username':user_id,
                 u'email':user_login.getProperty('email'),
                 u'name':user_id}

        if user_login.getProperty('fullname'):
            dados['name'] = user_login.getProperty('fullname')

        user_schema.createUserProfile(dados)


    else:
        user_data =  tools.get_prefs_user(user_id)
        if ((not user_data.get('name')) or (not user_data.get('date_birth')) or\
            (not user_data.get('phone_number')) or (not user_data.get('email'))) and alert_first_access:
            tools.setLogger('info',"Dados Incompletos no myvindula")