# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from vindula.myvindula.user import BaseFunc
from vindula.myvindula.models.photo_user import ModelsPhotoUser

import json

# Metodo que criar o usuario no acl_user do plone 
class VindulaWebServeExportPhotoUser(grok.View,BaseFunc):
    grok.context(Interface)
    grok.name('vindula-export-photouser')
    grok.require('zope2.View')

    retorno = {}

    def render(self):
        self.request.response.setHeader("Content-type","application/json")
        self.request.response.setHeader("charset", "UTF-8")
        return json.dumps(self.retorno,ensure_ascii=False)

    def update(self):
        dados = {}
        username = self.Convert_utf8(self.request.form.get('username',''))
        field = u'photograph'

        campo_image = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(username,field)

        if campo_image:
            dados['photograph'] = campo_image.photograph
            dados['thumb'] = campo_image.thumb

        self.retorno = dados
