# coding=utf-8
from five import grok
from zope import schema
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from vindula.content import MessageFactory as _
#from plone.namedfile import field
from plone.namedfile.field import NamedImage

from zope.interface import Interface

# Interface and schema
class IVindulaPhotoUser(form.Schema):
    """ Vindula Photo User """
    
#    title = schema.TextLine(
#        title=_(u"Título"),
#        description=_(u"Título para a imagem do Usuario"),)
    
    photograph = NamedImage(title=_(u"Foto"),
                            description=_(u"Coloque a foto do Usuario"),
                            required=False,
                                      )

   
class VindulaPhotoUserView(grok.View):
    grok.context(IVindulaPhotoUser)
    grok.require('zope2.View')
    grok.name('view')