# coding: utf-8
from five import grok
from zope.interface import Interface

from vindula.myvindula.tools.utils import UtilMyvindula

from urllib2 import urlopen

class MacroSingleComment(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-single-comment')
    
class MyVindulaCommentsMacro(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-comments-macro') 

class MacroInputComments(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-input-comments')

class MacroInputHowareu(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-input-howareu')

class MacroInputRecados(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-input-recados')
    
class MacroCommentsMaster(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-comments-master')    
    
class MacroSingleHowareu(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-single-howareu')    
    
class MyVindulaLikeMacro(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-like-macro')      

class MyVindulaDocumentByLineMacro(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('macro-myvindula-documentByLine')          
    
class MyVindulaImageView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-image_view')
    
class MacroImageProfilesUserView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-imageprofiles-macro')
    
class MyVindulaUserPerfil(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-user-perfil')
    
    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')
            
class MyVindulaImageUserLoad(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('image-user-load')
    
    def render(self):
        pass
    
    def update(self):
        open_for_anonymousUser =  self.context.restrictedTraverse('myvindula-conf-userpanel').check_myvindulaprivate_isanonymous();
        if open_for_anonymousUser:
            self.request.response.redirect(self.context.absolute_url() + '/login')            
            
        user = self.request.form.get('user','')
        url = self.getURLFotoUser(user)
        
        print url
        
        self.request.response.redirect(url,302)
        
