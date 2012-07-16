# coding: utf-8

from vindula.myvindula.user import BaseFunc,ModelsFuncDetails
from vindula.myvindula.user_photo import ModelsPhotoUser
from zope.app.component.hooks import getSite

import hashlib, urllib, base64

class UtilMyvindula(BaseFunc):
    
    def encodeUser(self,user):
        return base64.b16encode(user)
    
    def get_prefs_user(self, user):
        try:
            user_id = unicode(user, 'utf-8')    
        except:
            user_id = user 

        return ModelsFuncDetails().get_FuncDetails(user_id) 

    
    def checa_login(self):
        membership = self.context.portal_membership
        groups = self.context.portal_groups
        
        user_login = membership.getAuthenticatedMember()
        user_groups = groups.getGroupsByUserId(user_login.getId())
        
        checa = False
        if 'Manager' in user_login.getRoles():
            checa = True
        else:
            for i in user_groups:
                if i.id == 'manage-user':
                    checa = True 
                    break
        
        return checa       
    
    
    def getURLFotoUser(self,username):
        ativa_gravatar = self.context.restrictedTraverse('myvindula-conf-userpanel').check_ativa_gravatar()
        
        try: username = unicode(username)
        except: pass  
        campo_image = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(username)
        dados_user = ModelsFuncDetails().get_FuncDetails(username)
        
        if campo_image:
            return self.context.portal_url() + '/user-image?username='+username
                
        elif ativa_gravatar and dados_user:
            if dados_user.email:
                return self.loadGravatarImage(dados_user.email,username)
            elif dados_user.photograph:
                local = dados_user.photograph.split('/')
                try:
                    ctx= getSite()[local[0]][local[1]][local[2]]
                    obj = ctx.restrictedTraverse('@@images').scale('photograph', height=150, width=120)
                    return obj.url
                except:
                    pass

        return self.context.portal_url() + '/user-image?username='+username
        
        
        
    def loadGravatarImage(self, email,username): 
        # Imagem Padrão o usuario
        default = self.context.portal_url() + '/user-image?username='+username
        size = 168
        
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default,'s':str(size)})
        
        return gravatar_url       