# coding: utf-8
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import Interface

from plone.namedfile.field import NamedImage
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
from PIL import Image

from vindula.myvindula.user import ModelsFuncDetails

#Imports regarding the connection of the database 'strom'
from storm.locals import *
from storm.locals import Store
from vindula.myvindula.user import BaseFunc, BaseStore
from vindula.myvindula import PROJECT_ROOT_PATH
import pickle, StringIO

class ModelsPhotoUser(Storm, BaseStore):    
    __storm_table__ = 'vin_myvindula_photo_user'
    
    id = Int(primary=True)
    username = Unicode()
    date_creation = DateTime()
    photograph = Pickle()
    thumb = Pickle()
        
    def set_ModelsPhotoUser(self, **kwargs):
        # adicionando...
        setup = ModelsPhotoUser(**kwargs)
        self.store.add(setup)
        self.store.flush()
        return setup.id          
    
    def del_ModelsPhotoUser(self, username):
        result = self.get_ModelsPhotoUser_byUsername(username)
        if result:
            self.store.remove(result)
            self.store.flush()

    
    def get_ModelsPhotoUser_byID(self,id):
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.id == id).one()
        if data:
            return data
        else:
            return None

    def get_ModelsPhotoUser_byUsername(self,username):
        data = self.store.find(ModelsPhotoUser, ModelsPhotoUser.username == username).one()
        if data:
            return data
        else:
            return None



class MyVindulaUserCropImageView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-user-crop')

    def update(self):
        """ Receive itself from request and do some actions """
        form = self.request.form
        submitted = form.get('form.submitted', False)
        croped = form.get('form.crop', False)
        self.error = ''
        
        if submitted:
            try:username = unicode(form.get('username',''))
            except:username = form.get('username','')  

            if form['photo'].filename != '':
                photo = form.get('photo',None)    
                filename = photo.filename # pega o nome do arquivo
                if filename.endswith('png') or filename.endswith('PNG') or\
                   filename.endswith('jpg') or filename.endswith('JPG') or\
                    filename.endswith('gif')  or filename.endswith('GIF'):    
                    
                    data = photo.read()       
                    img_org = Image.open(StringIO.StringIO(data))
                    # verifica se a imagem é maior que o máximo permitido
                    tamMax = (640.0,440.0)
                    imgSize = img_org.size
                    if (imgSize[0] > tamMax[0]) or (imgSize[1] > tamMax[1]):
                        #verifica se a largura é maior que a altura
                        if (imgSize[0] > imgSize[1]):
                            novaLargura = tamMax[0]
                            novaAltura = round((novaLargura / imgSize[0]) * imgSize[1])
                        elif (imgSize[1] > imgSize[0]):
                            #se a altura for maior que a largura
                            novaAltura = tamMax[1]
                            novaLargura = round((novaAltura / imgSize[1]) * imgSize[0])
                        else:
                            #altura == largura
                            novaAltura = novaLargura = max(tamMax)
                    
                        img_org.thumbnail((novaLargura, novaAltura), Image.ANTIALIAS)

                        
                    imagefile = StringIO.StringIO()
                    img_org.save(imagefile,'JPEG')
                    buffer = imagefile.getvalue() 
                                     
                    M ={}
                    M['data'] = buffer
                    M['filename'] = filename                        
                    photograph = pickle.dumps(M)
                    
                    check_user = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(username) 
                    if not check_user:
                        D = {}
                        D['username'] = username 
                        D['photograph'] = photograph           
                        
                        self.id_photo = ModelsPhotoUser().set_ModelsPhotoUser(**D)
                    
                    else:
                        check_user.photograph = photograph
                        self.id_photo = check_user.id
                else:
                    self.error = 'Arquivo não suportado, insira um arquivo de imagem.' 
            else:
                self.error = 'Insira um arquivo de imagem.'
                    
        elif croped:
            try:username = unicode(form.get('username',''))
            except:username = form.get('username','')
            id = form.get('id','')
            
            imagem_data = campo_image = ModelsPhotoUser().get_ModelsPhotoUser_byID(int(id))
            if imagem_data:
                image = imagem_data.photograph
                photograph =  pickle.loads(image)
                imagem = photograph.get('data','')
            else:
                imagem = ''
            
            cort_x = int(form.get('cort-x',''))
            cort_y = int(form.get('cort-y',''))

            cort_x2 = int(form.get('cort-x2',''))
            cort_y2 = int(form.get('cort-y2',''))
            box = (cort_x, cort_y, cort_x2, cort_y2)
            
            img = Image.open(StringIO.StringIO(imagem))
            
            area = img.crop(box)
            #area.thumbnail((168, 168), Image.ANTIALIAS)
            area = area.resize((168, 168), Image.ANTIALIAS)
            if imagem_data:
                imagefilecrop = StringIO.StringIO()
                area.save(imagefilecrop,'JPEG')
                
                M ={}
                M['data'] = imagefilecrop.getvalue() 
                M['filename'] = 'crop_'+photograph.get('filename','')                    
                imagem_data.thumb = pickle.dumps(M)
                
                self.id_photo = imagem_data.id

#Views de renderização das Image dos usuario ---------------------------------------------------   
class MyVindulaUserImage(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('user-image')
    
    def render(self):
        pass
    
    def update(self):
        form = self.request.form

        if 'id' in form.keys():
            id = form.get('id','0')
            campo_image = ModelsPhotoUser().get_ModelsPhotoUser_byID(int(id))

        elif 'username' in form.keys():
            try: username = unicode(form.get('username',''))
            except: username = form.get('username','')  
            campo_image = ModelsPhotoUser().get_ModelsPhotoUser_byUsername(username)
            dados_user = ModelsFuncDetails().get_FuncDetails(username)
            
        else:
            campo_image = None
            dados_user = None

        if campo_image:
            if 'full' in form.keys():
                image = campo_image.photograph
            else:    
                image = campo_image.thumb
            
            x =  pickle.loads(image)
            filename = x['filename']
            self.request.response.setHeader("Content-Type", "image/jpeg", 0)
            #self.request.response.setHeader('Content-Disposition','attachment; filename=%s'%(filename))
            self.request.response.write(x['data'])
        
        elif dados_user:
            if dados_user.photograph:
                local = dados_user.photograph.split('/')
                try:
                    objeto = getSite()[local[0]][local[1]][local[2]]
                    if objeto.photograph:
                        self.request.response.setHeader("Content-Type", "image/jpeg", 0)
                        self.request.response.write(objeto.photograph.data)        
                except:
                    self.loadDefault()
            else:
                self.loadDefault()
        else:
            self.loadDefault()
            

    def loadDefault(self):
        defaulUser = PROJECT_ROOT_PATH + '/static/images/defaultUser.png'
        try:
            file = open(defaulUser,'r')
            buffer = file.read()
        except:
            buffer = ''
        
        self.request.response.write(buffer)
        


#Views de eclução da Image do usuario ---------------------------------------------------   
class MyVindulaUserDelImage(grok.View, BaseFunc):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula-user-delcrop')
    
    def update(self):
        form = self.request.form

        if 'form.excluir' in form.keys():
            try: username = unicode(form.get('username',''))
            except: username = form.get('username','')  
              
            ModelsPhotoUser().del_ModelsPhotoUser(username)
            
            
            