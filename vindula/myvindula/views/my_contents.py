# coding: utf-8
from five import grok
from zope.interface import Interface

from Products.CMFCore.utils import getToolByName


grok.templatedir('templates')

class MyContentsView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('myvindula_my_contents')

    def get_conteudos(self):
        context = self.context
        query = {}
        member =  context.restrictedTraverse('@@plone_portal_state').member()

        username = member.getUserName();

        portal_catalog = getToolByName(context, 'portal_catalog')
        path = context.portal_url.getPortalObject().getPhysicalPath()

        query.update({'path': {'query':'/'.join(path)},
                     'sort_on':'created',
                     'sort_order':'descending',
                     'Creator':username,
                     })

        return portal_catalog(**query)


    def get_title_WF(self,review_state,obj):
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        return portal_workflow.getTitleForStateOnType(review_state, obj.portal_type)