# coding: utf-8

from vindula.myvindula.user import BaseFunc,ModelsFuncDetails


class UtilMyvindula(BaseFunc):
    
    def get_prefs_user(self, user):
        try:
            user_id = unicode(user, 'utf-8')    
        except:
            user_id = user 

        return ModelsFuncDetails().get_FuncDetails(user_id)    