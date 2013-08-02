# coding: utf-8

from Products.statusmessages.interfaces import IStatusMessage
from vindula.myvindula import MessageFactory as _


#from vindula.myvindula.models.funcdetails import ModelsFuncDetails
from vindula.myvindula.models.photo_user import ModelsPhotoUser

from vindula.myvindula.models.base import BaseStore

# Import para envio de E-mail
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email import Encoders
from vindula.myvindula.tools.layoutemail import LayoutEmail


from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

import hashlib, urllib, base64, pickle
from datetime import date, datetime

import logging
logger = logging.getLogger('vindula.myvindula')

class UtilMyvindula(object):

    def __init__(self):
        self.site = getSite()
        
        self.catalog = getToolByName(self.site, 'portal_catalog')
        self.portal_url = getToolByName(self.site, 'portal_url')
        self.membership = self.site.portal_membership
        
        self.db = BaseStore()    
            
    
    def encodeUser(self,user):
        return base64.b16encode(user)
    
    def decodeUser(self,hash):
        return base64.b16decode(hash)
        
    
    def get_prefs_user(self, user):
        from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
        from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
        user_id = self.Convert_utf8(user)
        #return ModelsFuncDetails().get_FuncDetails(user_id)

        campos = ModelsConfgMyvindula().get_configurationAll()
        dados = ModelsInstanceFuncdetails().get_InstanceFuncdetails(user_id)
        
        D = {}
        if dados:
            D['instance_user'] = dados.id
        for campo in campos:
            D[campo.fields] = self.getDadoUser_byField(dados, campo.fields)
        
        return D
        
    def get_Dic_Campos(self):
        from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula
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
    
    def getDadoUser_byField(self,instanceUser,campo):
        if instanceUser:
            tmp = instanceUser.dadosUses.find(vin_myvindula_confgfuncdetails_fields=self.Convert_utf8(campo)).one()
            if tmp:
                try:data = self.decodePickle(tmp.valor)
                except:data = tmp.valor
                if type(data) == list:
                    str = ''
                    for i in data:
                        if i:str += i +' / '
                    
                    data = str
                return data
        return None
     

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
        
        if request.other.get('came_from') in (getSite().portal_url()+'/', '', None):
            request.other["came_from"]=url
        
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
    
    
    def getURLFotoUser(self,username):
        ativa_gravatar = self.context.restrictedTraverse('myvindula-conf-userpanel').check_ativa_gravatar()
        
        username = self.Convert_utf8(username)
        campo_image = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(username)
        dados_user = self.get_prefs_user(username)# ModelsFuncDetails().get_FuncDetails(username)
        
        if campo_image:
            return self.context.portal_url() + '/user-image?username='+username+'&field=photograph'
                
        elif ativa_gravatar and dados_user:
            if dados_user.get('email',False):
                return self.loadGravatarImage(dados_user.get('email',''),username)
            elif dados_user.get('photograph',False):
                local = dados_user.get('photograph','').split('/')
                try:
                    ctx= getSite()[local[0]][local[1]][local[2]]
                    obj = ctx.restrictedTraverse('@@images').scale('photograph', height=150, width=120)
                    return obj.url
                except:
                    pass

        return self.context.portal_url() + '/user-image?username='+username+'&field=photograph'
        
        
        
    def loadGravatarImage(self, email,username): 
        # Imagem Padrão o usuario
        default = self.context.portal_url() + '/user-image?username='+username+'&field=photograph'
        size = 168
        
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default,'s':str(size)})
        
        return gravatar_url       


    def envia_email(self,ctx, msg, assunto, mail_para, arquivos=[],to_email=None):
        """
        Parte do codigo retirado de:
            - http://dev.plone.org/collective/browser/ATContentTypes/branches/release-1_0-branch/lib/imagetransform.py?rev=10162
            - http://www.thescripts.com/forum/thread22918.html
            - http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473810
        """

        portal = getSite()

        # Cria a mensagem raiz, configurando os campos necessarios para envio da mensagem.
        mensagem = MIMEMultipart('related')
        mensagem['Subject'] = assunto

        #Pega os remetentes do email pelas configurações do zope @@mail-controlpanel
        if to_email:
            mensagem['From'] = '%s <%s>' % (to_email,to_email)
        else:
            mensagem['From'] = '%s <%s>' % (portal.getProperty('email_from_name'),
                                            portal.getProperty('email_from_address'))

        mensagem['To'] = mail_para
        mensagem.preamble = 'This is a multi-part message in MIME format.'


        email_layout_obj = LayoutEmail(msg=msg, ctx=ctx)        
        mensagem.attach(MIMEText(email_layout_obj.layout(), 'html', 'utf-8'))
        
        # Atacha os arquivos
        for f in arquivos:
            if type(f) == dict:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(f.get('data',f))
                Encoders.encode_base64(parte)
                parte.add_header('Content-Disposition', 'attachment; filename="%s"' % f.get('filename','image.jpeg'))

                mensagem.attach(parte)

        mail_de = mensagem['From']

        #Pegando SmtpHost Padrão do Plone
        smtp_host   = portal.MailHost.smtp_host
        smtp_port   = portal.MailHost.smtp_port
        smtp_userid = portal.MailHost.smtp_uid
        smtp_pass   = portal.MailHost.smtp_pwd
        server_all  = '%s:%s'%(smtp_host,smtp_port)

        smtp = smtplib.SMTP()
        try:
            smtp.connect(server_all)
            #Caso o Usuario e Senha estejam preenchdos faz o login
            if smtp_userid and smtp_pass:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(smtp_userid, smtp_pass)
                except:
                    smtp.login(smtp_userid, smtp_pass)

            smtp.sendmail(mail_de, mail_para, mensagem.as_string())
            smtp.quit()
        except:
            return False

        return True