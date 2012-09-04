# coding: utf-8
from five import grok
from plone.directives import form

from zope import schema
from z3c.form import button
from plone import namedfile

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.dexterity.utils import createContentInContainer

from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone.scale.storage import IImageScaleStorage

from vindula.myvindula import MessageFactory as _




from storm.locals import *

from vindula.myvindula.validation import valida_form
from datetime import date
from copy import copy 
import pickle


from vindula.myvindula.models.base import BaseStore
from vindula.myvindula.models.funcdetails import ModelsFuncDetails
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
from vindula.myvindula.models.department import ModelsDepartment
from vindula.myvindula.models.howareu import ModelsMyvindulaHowareu
from vindula.myvindula.models.comments import ModelsMyvindulaComments
from vindula.myvindula.models.like import ModelsMyvindulaLike
from vindula.myvindula.models.funcdetail_couses import ModelsMyvindulaFuncdetailCouses
from vindula.myvindula.models.courses import ModelsMyvindulaCourses
from vindula.myvindula.models.funcdetail_languages import ModelsMyvindulaFuncdetailLanguages
from vindula.myvindula.models.languages import ModelsMyvindulaLanguages
from vindula.myvindula.models.recados import ModelsMyvindulaRecados

from vindula.myvindula.models.holerite import ModelsFuncHolerite
from vindula.myvindula.models.descricao_holerite import ModelsFuncHoleriteDescricao
from vindula.myvindula.models.photo_user import ModelsPhotoUser


from vindula.myvindula.tools.utils import UtilMyvindula


class UserLogado(grok.Permission):
    grok.name('vindula.UserLogado')

    
        
class BaseFunc(UtilMyvindula):
    #default class for standard functions

            
    def converte_dadosByDB(self, D):
        keys = D.keys()
        for item in keys:
            if item == 'itens_holerite' or\
               item == 'itens_holerite_check' or\
               item == 'completo':
                D.pop(item)
            else: 
                valor = D[item]
                if type(valor) == str: 
                    valor = valor.strip()
                    try:
                        D[item] = unicode(valor, 'utf-8')
                    except:
                        D[item] = unicode(valor, 'ISO-8859-1')
                else:
                    D[item] = valor
        
        return D


    def geraCampos(self,form_data):
        if type(form_data) == dict:
            errors = form_data.get('errors',[])
            data = form_data.get('data',[])
            campos = form_data.get('campos',[])
            value_choice = form_data.get('lista_itens',{})
            
            manage = form_data.get('manage',False)
            config_myvindula = form_data.get('config_myvindula',{})
            

            FIELD_BLACKLIST = ['username',
                               'vin_myvindula_department',
                               ]
            
            html=[]
            
            camposAux = copy(campos)
            for item in camposAux:
                if item in FIELD_BLACKLIST:
                    campos.pop(item)
                else:    
                    html.append(campos[item].get('ordem',0))

            html.sort()
            
            for campo in campos.keys():
                index = campos[campo].get('ordem',0)
                tmp = ""
 
                if self.checaEstado(config_myvindula,campo) or manage:
                    type_campo = campos[campo]['type']
                else:
                    type_campo = 'hidden'
                
                mascara_campo = campos[campo].get('mascara',None)
                if mascara_campo:
                    mascara="onKeyDown='Mascara(this,{0});' onKeyPress='Mascara(this,{0});' onKeyUp='Mascara(this,{0});'".format(mascara_campo)
                else:
                    mascara = ''
                
                tmp += "<!-- Campo %s -->"%(campo)
                tmp += "<div class='%s' id='%s' >"%(self.field_class(errors, campo),"field-"+campo)
                
                if type_campo != 'hidden':
                    tmp += "   <label for='%s'>%s</label>"%(campo,campos[campo].get('label',''))
                    if campos[campo]['required'] == True and type_campo != 'hidden':
                        tmp += "   <span class='fieldRequired' title='Obrigatório'>(Obrigatório)</span>"
    
                    tmp += "   <div class='formHelp'>%s</div>"%(campos[campo]['decription'] or '')
                    tmp += "   <div >%s</div>"%(errors.get(campo,''))
                
                if type_campo == 'hidden':
                    tmp += "<input id='%s' type='hidden' value='%s' name='%s' size='25'/>"%(campo,self.getValue(campo,self.request,data),campo)
                
                elif type_campo == 'img':
                   
                    url = getSite().portal_url()
                    instance = campos[campo].get('instance_id','0')
                    user_foto = ModelsPhotoUser().get_ModelsPhotoUser_byFieldAndInstance(self.Convert_utf8(campo),int(instance))
                    
                    tmp +="<div id='%s'><a href='%s/myvindula-user-crop?field=%s&instance_id=%s' class='crop-foto' id='%s'>Editar Foto</a>" %(campo,url,campo,instance,campo)
                    if user_foto:
                        tmp += "<div id='preview-user-%s'><img height='150px' src='%s/user-image?field=%s&instance_id=%s' /></div>" %(campo,url,campo,instance)
                        tmp += "<a href='%s/myvindula-user-delcrop?field=%s&instance_id=%s' class='excluir-foto'>Excluir Foto</a>" %(url,campo,instance)
                    
                    else:
                        tmp += "<div id='preview-user-%s'></div>"%(campo)
                        tmp += "<a href='%s/myvindula-user-delcrop?field=%s&instance_id=%s' style='display:none' class='excluir-foto'>Excluir Foto</a>" %(url,campo,instance)
                    
                    tmp += "</div>"
                
                elif type_campo == 'file':
                    if errors:
                        if self.getFile(campo,self.request,data):
                            tmp += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(campo,self.request,data))
                    else:
                        if self.getFile(campo,self.request,data):
                            tmp += "<a href='%s' target='_blank'>Download do Arquivo</a><br />"%(self.getFile(campo,self.request,data))
                    tmp += "<input id='%s' type='file' value='%s' name='%s' size='25' />"%(campo,self.getFile(campo,self.request,data),campo)
                
                elif type_campo == 'date':
                    tmp += """<input id='%s' type='text' maxlength='10' onKeyDown='Mascara(this,Data);' onKeyPress='Mascara(this,Data);' onKeyUp='Mascara(this,Data);'
                                     value='%s' name='%s' size='25'/>"""%(campo,self.converte_data(self.getValue(campo,self.request,data),True),campo)
    
                elif type_campo == 'textarea':
                    tmp += "<textarea id='%s' name='%s' style='width: 100; height: 81px;'>%s</textarea>"%(campo, campo, self.getValue(campo,self.request,data)) 
                
                elif type_campo == 'bool':
                    tmp += "<input id='%s' type='checkbox' value='%s' name='%s' size='25' %s/>"%(campo,'True',campo,self.checked(campo,self.request,data))
                
                elif type_campo == 'combo':
                    select = False
                    tmp += "<select name='%s'>"%(campo) 
                    tmp += "<option value="">-- Selecione --</option>"
                    for item in value_choice[campo]:
                        if item[0] == self.getValue(campo,self.request,data):
                            select = True
                            tmp +="<option value='%s' selected>%s</option>"%(item[0], item[1])
                        else:
                            tmp +="<option value='%s'>%s</option>"%(item[0], item[1])
                    tmp += "</select>"
                    if select:
                        tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo,'', campo)
                    else:
                        tmp += "<input id='%s' type='text' value='%s' name='%s' size='25'/>"%(campo, self.getValue(campo, self.request,data), campo)
                
                elif type_campo == 'list':
                    tmp += "<div class='boxSelecao' name='%s'>"%(campo)
                    for item in value_choice[campo]:
                        lable =  item[1]
                        valueList = self.getValueList(campo,self.request,data)
                        if valueList and item[0] in valueList:
                            tmp += "<input value='%s' type='checkbox' checked name='%s'/><label>%s</label><br/>"%(item[0],campo,lable)
                        else:
                            tmp += "<input value='%s' type='checkbox' name='%s'/><label>%s</label><br/>"%(item[0],campo,lable)
                    tmp += "</div>" 
                
                elif type_campo == 'choice':
                    tmp += "<select name='%s'>"%(campo)
                    tmp += "<option value="">-- Selecione --</option>"
                    for item in value_choice[campo]:
                        if item[0] == self.getValue(campo,self.request,data):
                            tmp +="<option value='%s' selected>%s</option>"%(item[0], item[1])
                        else:
                            tmp +="<option value='%s'>%s</option>"%(item[0], item[1])

                    tmp += "</select>"
             
                else:
                    tmp += "<input id='%s' type='text' value='%s' name='%s' size='25' %s/>"%(campo, self.getValue(campo, self.request,data), campo,mascara)

                tmp += "</div>"
                
                pos = html.index(index)
                html.pop(pos)
                html.insert(pos, tmp)  
                
            
            return html

        
    def geraExtraCampos(self,form_data):
        if type(form_data) == dict:
            errors = form_data.get('errors',None)
            data = form_data.get('data',None)
            campos = form_data.get('campos',None)
            
            html=[]
            i=0
            while i < len(campos.keys()):
                html.append(i)
                i+=1
            for campo in campos.keys():
                
                mascara_campo = campos[campo].get('mascara',None)
                if mascara_campo:
                    mascara="onKeyDown='Mascara(this,{0});' onKeyPress='Mascara(this,{0});' onKeyUp='Mascara(this,{0});'".format(mascara_campo)
                else:
                    mascara = ''
                
                type_campo = campos[campo]['type']
                index = campos[campo].get('ordem',0)
                tmp = ""
                tmp += "<!-- Campo %s -->"%(campo)
                tmp += "<div class='%s'>"%(self.field_class(errors, campo))
                tmp += "   <label for='%s'>%s</label>"%(campo,campos[campo]['label'])
                
                if campos[campo]['required'] == True:
                    tmp += "   <span class='fieldRequired' title='Obrigatório'>(Obrigatório)</span>"

                tmp += "   <div class='formHelp'>%s.</div>"%(campos[campo]['decription'])   
                tmp += "   <div >%s</div>"%(errors.get(campo,''))
                if type_campo == 'file':
                    if campo == 'logo_corporate' and data:
                        tmp += "<img src='%s' height='60px'/><br />" %( getSite().portal_url() +'/company-logo?cnpj='+data.get('cnpj',''))
                    
                    tmp += "<input id='%s' type='file' value='%s' name='%s' size='25'  accept='image/*'/>"%(campo,'',campo)
                else:
                    tmp += "<input id='%s' type='text' value='%s' name='%s' size='25' %s />"%(campo,self.getValue(campo,self.request,data),campo,mascara)
                
                tmp += "</div>"
                html.pop(index)
                html.insert(index, tmp)    
            
            return html
