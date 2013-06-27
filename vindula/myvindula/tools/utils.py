# coding: utf-8

from Products.statusmessages.interfaces import IStatusMessage
from vindula.myvindula import MessageFactory as _


# from vindula.myvindula.models.photo_user import ModelsPhotoUser

from vindula.myvindula.models.base import BaseStore

from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula


from vindula.myvindula.tools.ago import human


from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

import hashlib, urllib, base64, pickle
from datetime import date, datetime

import pytz
import logging
logger = logging.getLogger('vindula.myvindula')

class UtilMyvindula(object):

    def __init__(self):
        self.site = getSite()

        self.catalog = getToolByName(self.site, 'portal_catalog')
        self.rtool = getToolByName(self.site, 'reference_catalog')
        self.portal_url = getToolByName(self.site, 'portal_url')
        self.membership = self.site.portal_membership

        self.db = BaseStore()

    def encodeUser(self,user):
        return base64.b16encode(user)

    def decodeUser(self,hash):
        return base64.b16decode(hash)


    def get_prefs_user(self, user):
        # from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
        from vindula.myvindula.models.funcdetails import FuncDetails
        return FuncDetails(self.Convert_utf8(user))

    # def get_prefs_user(self, user):
    #     user_id = self.Convert_utf8(user)
    #     campos = ModelsConfgMyvindula().get_configurationAll()

    #     D = {'username':user_id}

    #     for campo in campos:
    #         D[campo.name] = self.getDadoUser_byField(user_id, campo.name)

    #     return D

    def get_Dic_Campos(self):
        campos = {}
        fields = ModelsConfgMyvindula().get_configurationAll()
        if fields:
            for field in fields:
                if not field.fields in ['vin_myvindula_department']:
                    M={}
                    M['required'] = field.required
                    M['type'] = field.type
                    M['label'] = field.label
                    M['decription'] = field.decription
                    M['ordem'] = field.ordem
                    M['mascara'] = field.mascara

                    campos[field.fields] = M

        return campos

    # def getDadoUser_byField(self,user,campo):

    #     # TODO: Corrigir esse metodo. Esta retornando informacao valida, mas com sintaxe ruim.

    #     from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails

    #     usuario = unicode(user)
    #     result = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndFieldName(usuario,campo)


    #     if result:
    #         return result.value
    #     else:
    #         return []


    # def getDadoUser_byFieldName(self,user,campo):

    #     # TODO: Corrigir esse metodo. Esta retornando informacao valida, mas com sintaxe ruim.
    #     from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails

    #     usuario = unicode(user)
    #     result = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndFieldName(usuario,campo)


    #     if result:
    #         return result.value
    #     else:
    #         return []

    def lookupObject(self, uid):
        '''
            Passa o uid para retornar o objcet do plone
        '''
        return UtilMyvindula().rtool.lookupObject(uid)


    def getUnidadePrincipalSigla(self, usuario, m=0):

        # TODO: Corrigir esse metodo. Esta retornando informacao valida, mas com sintaxe ruim.
        # passar m=1 caso queira a sigla em maiuscula
        structure = self.get_prefs_user(usuario).get_unidadeprincipal()
        sigla = ''
        if structure:
            sigla = structure.getSiglaOrTitle()

        # sigla = sigla.replace('<p>','').replace('</p>','')
        if m == 1:
            return str(sigla).upper()
        else:
            return sigla


    def to_utf8(self, value):
        return unicode(value, 'utf-8')


    # define se aparece ou nao as mensagens e marcacoes de erros
    def field_class(self, errors, field_name):
        if errors is not None:
            if errors.get(field_name, None) is not None:
                return 'field error'
            else:
                 return 'field'
        else:
              return 'field'

    #pega o valor entre dois campos
    def checaValor(self, x, y):
        if not x and not y:
            return ''
        elif x:
             return x
        elif y:
             return y
        else:
             return ''

    def checaEstado(self,config, campo):
        if config:
            try:
                return config.get(campo)
            except:
                return True
        else:
            return True

    def decodePickle(self,valor):
        if valor:
            return pickle.loads(str(valor))
        else:
            return ''

    def encodePickle(self,valor):
        if valor:
            return pickle.dumps(valor)
        else:
            return u''

    def Convert_utf8(self,valor):
        try:
            return unicode(valor,'utf-8')
        except UnicodeDecodeError:
            return valor.decode("utf-8", "ignore")
        except:
            if type(valor) == unicode:
                return valor
            else:
                return u'erro ao converter os caracteres'

    def rs_to_list(self, rs):
        if rs:
            return [i for i in rs]

    def get_ip(self, request):
        """ Extract the client IP address from the HTTP request in a proxy-compatible way.

        @return: IP address as a string or None if not available
        """
        if "HTTP_X_FORWARDED_FOR" in request.environ:
            # Virtual host
            ip = request.environ["HTTP_X_FORWARDED_FOR"]
        elif "HTTP_HOST" in request.environ:
            # Non-virtualhost
            ip = request.environ["REMOTE_ADDR"]
        else:
            # Unit test code?
            ip = None

        return ip

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


    def getValue(self,campo,request,data):
        if campo in request.keys():
            if request.get(campo, None) != None:
                return request.get(campo,'')
            else:
                return ''
        elif campo in data.keys():
            if data.get(campo, None) != None:
                return data.get(campo,'')
            else:
                return ''
        else:
            return ''

    def getValueList(self,campo,request,data):
        if campo in request.keys():
            if request.get(campo, ''):
                return request.get(campo,[])
            else:
                return []
        elif data:
            L = data.get(campo,'')
            return L


    def getParametersFromURL(self, ctx):
        traverse = ctx.context.REQUEST.get('traverse_subpath')
        vars = {}
        if traverse != None:
            size = len(traverse)
            counter = 0
            for i in range(size/2):
                position = i+counter
                vars.update({traverse[position]:traverse[position+1]})
                counter+=1
        return vars

    def checked(self,campo,request,data,ativa='edit'):
        if campo in request.keys():
            if request.get(campo, '') == True or\
                request.get(campo,'') == 'True':
                return "checked"
            else:
                return ""
        elif campo in data.keys():
            if data.get(campo,'') == True or\
                data.get(campo,'') == 'True':
                return "checked"
            else:
                return ""
        else:
            return ""


    # retorna dado convertido para o campo de valor monetario
    def converte_valor(self, valor):
        if valor is not None:
            if type(valor) == Decimal:
                valor = str(valor)
                valor = valor.replace('R$ ','')
                valor = valor.replace('.', ',')
                #valor = 'R$ ' + valor
                return valor
            else:
                return None
        else:
            return None

    #retorno a data de competencia no ordem coreta
    def converte_competencia(self, valor):
        if valor is not None:
            tmp = valor.split('/')
            return tmp[1]+'/'+tmp[0]
        else:
            return None

    # retorna dado convertido para o campos de data
    def converte_data(self, data, data_atual=False):
        if data is not None and data != '':
            if type(data) == date:
                return data.strftime('%d/%m/%Y')
            else:
                return data
        else:
            if data_atual == True:
                data = date.today()
                dia = data.day
                mes = data.month
                ano = data.year

                if dia < 10:
                    dia = '0' + str(dia)
                else:
                    dia = str(dia)

                if mes < 10:
                    mes = '0' + str(mes)
                else:
                    mes = str(mes)

                datastr = dia + '/' + mes + '/' + str(ano)

                return datastr
            else:
                return data

#    #Retorna o label dos campos dinamicos
#    def get_label_filed(self, campo):
#        from vindula.myvindula.registration import SchemaConfgMyvindula
#        result = ModelsConfgMyvindula().get_configuration_By_fields(campo)
#        default = SchemaConfgMyvindula().campos.get(campo)
#
#        if result:
#            label = result.__getattribute__('label')
#            if not label:
#                return default.get('label')
#            else:
#                return label
#
#        else:
#            return default.get('label')

    def setLogger(self,type,msg):
        '''
        @types = info, warning
        @msg = mesagem para o gravar no log
        '''
        cmd = 'logger.%s("%s")'%(type,msg)
        try:
            eval(cmd)
        except:
            logger.warning("Erro ao executar o camando setLogger")


    def setStatusMessage(self,type,msg):
        '''
        @type = info, error, warning
        @msg = mesagem que sera apresentada ao usuario
        '''
        try:
            request = self.site.REQUEST
        except:
            request =self.context.REQUEST
        IStatusMessage(request).addStatusMessage(_(self.to_utf8(msg)), type)


    def setRedirectPage(self,local):
        '''
        @local = caminho relativo ao portal para redirecionar o usuario
        '''
        try:
            site = self.site
        except:
            site =self.context
        url = site.absolute_url() + local
        request = site.REQUEST
        request.response.redirect(url, lock=True)



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

    def getTimeAgo(self,time,texto='Acessado'):
        # to find out how long ago, use the human function
        return texto + human(time)


    def getURLFotoUser(self,username,field='photograph'):
        ativa_gravatar = self.context.restrictedTraverse('myvindula-conf-userpanel').check_ativa_gravatar()
        username = self.Convert_utf8(username)

        return self.context.portal_url() + '/vindula-api/myvindula/user-picture/'+field+'/'+username+'/'+str(ativa_gravatar)

    def now():
        #TODO: COLOCAR ESSA CONFIGURACAO NUM LUGAR MELHOR
        #MYSQL=1
        #POSTGRES=2
        DB = 1
        if DB == 1:
            return datetime.now()
        elif DB == 2:
            return datetime.now(pytz.utc)
            

    # def loadGravatarImage(self, email,username):
    #     # Imagem Padrão o usuario
    #     default = self.context.portal_url() + '/vindula-api/myvindula/user-picture/photograph/'+username+'/'
    #     size = 168

    #     gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    #     gravatar_url += urllib.urlencode({'d':default,'s':str(size)})

    #     return gravatar_url
