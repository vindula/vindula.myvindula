# coding: utf-8
# from five import grok
# from zope.interface import Interface

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from Acquisition import aq_inner

from vindula.myvindula.tools.utils import UtilMyvindula

from vindula.myvindula.models.instance_funcdetail import ModelsInstanceFuncdetails
from vindula.myvindula.models.dados_funcdetail import ModelsDadosFuncdetails
from vindula.myvindula.models.confgfuncdetails import ModelsConfgMyvindula

   
def Convert_utf8(valor):
    try: 
        return unicode(valor,'utf-8')
    except UnicodeDecodeError:
        # return valor.decode("utf-8", "ignore")
        return valor.decode('iso-8859-2').decode('utf8')
    except:
        if type(valor) == unicode:
            return valor
        else:
            return u'erro ao converter os caracteres'

def remove_list(lista):
	if isinstance(lista, list):
		return lista[0]
	else:
		return lista

class SyncLdalMyvindula(object):

	def __init__(self, context, request):
		self.context = context
		self.request = request

	def update_data_user(self,username, dados):
		user_instance = ModelsInstanceFuncdetails().get_InstanceFuncdetails(username)
		if not user_instance:
			user_instance = ModelsInstanceFuncdetails().set_InstanceFuncdetails(username)
		else:
			user_instance = user_instance.id

		for campo in dados.keys():
			field_name = Convert_utf8(campo)
			myvindula_fields = ModelsConfgMyvindula().get_configuration_By_fields(field_name)
			
			if myvindula_fields:
				valor = Convert_utf8(dados.get(campo,''))
				result_campo = ModelsDadosFuncdetails().get_DadosFuncdetails_byInstanceAndField(user_instance,field_name)
				
				if result_campo:
					if result_campo.valor != valor:
						result_campo.valor = valor
						ModelsDadosFuncdetails().store.commit()
				else:
					D={}
					D['vin_myvindula_instance_id'] = user_instance
					D['vin_myvindula_confgfuncdetails_fields'] = field_name
					D['valor'] = valor

					ModelsDadosFuncdetails().set_DadosFuncdetails(**D)

	def sync_user(self,username):
		searchView = getMultiAdapter((aq_inner(self.context), self.request), name='pas_search')
			
		search_user = searchView.searchUsers(**{'login':username})
		if search_user:
			search_user = search_user[0]
			connector  = self._get_connector(search_user.get('pluginid',''))
			if connector:
				user_dn = search_user.get('dn','')
				acl_user = connector.acl_users
				if hasattr(acl_user, 'getUserDetails'):
					details_user = acl_user.getUserDetails(encoded_dn=user_dn, format='dictionary')
					self._manager_details(connector,details_user)

				


	def _manager_details(self, connetor, dados_user):
		schema_ldap = connetor.acl_users.getLDAPSchema()
		schema_map_ldap = connetor.acl_users.getMappedUserAttrs()

		D = {}
		for schema in schema_map_ldap:
			chave_ldap = schema[0]
			chave_myvindula = schema[1]
			
			#DE/PARA dos campos padrão do conector do ad
			#Nome do usuario
			if chave_myvindula in ['first_name','last_name']:
				D['name'] = '%s %s' %(remove_list(dados_user.get('givenName','')),
									  remove_list(dados_user.get('sn',''))
									  )
			#Login do usuario
			elif chave_myvindula == 'windows_login_name':
				D['username'] = remove_list(dados_user.get(chave_ldap,''))

			#DE/PARA dos campos padrão do conector do Ldap
			#Nome do Usuario
			elif chave_myvindula in ['fullname',]:
				D['name'] = remove_list(dados_user.get('cn',''))

			else:
				D[chave_myvindula] = remove_list(dados_user.get(chave_ldap,''))

		#Login do usuario
		if not 'username' in D.keys():
			D['username'] = remove_list(dados_user.get('uid',''))

		username = Convert_utf8(D.get('username', ''))
		self.update_data_user(username, D)

		return True

	def _get_connector(self,pluginid):
		acl_users = getToolByName(self.context, 'acl_users')
		try:
			return acl_users[pluginid]
		except:
			return None

	def sync_all_user(self):
		acl_users = getToolByName(self.context, 'acl_users')
		itens = [item for item in acl_users.objectValues()\
				       if item.meta_type == 'Plone Active Directory plugin' or\
				          item.meta_type == 'Plone LDAP plugin']

		L =[]
		for iten in itens:
			user_ldap = iten.acl_users.findUser('cn','')

			for user in user_ldap:
				self._manager_details(iten,user )
