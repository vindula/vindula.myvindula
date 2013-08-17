# -*- coding: utf-8 -*-

class LayoutEmail(object):
	"""docstring for LayoutEmail"""

	def __init__(self, msg, ctx):
		super(LayoutEmail, self).__init__()
		themeconfig = ctx.restrictedTraverse('personal-layout.css')

		config = themeconfig.getConfiguration()[0]


		self.conteudo = msg 

		self.url_logo_topo = config.get('logo_portal')
		self.url_logo_radape = config.get('logo_footer')
		self.url_banner = config.get('banner_topo')


	def layout (self):
		banner = ''
		if  self.url_banner:
			banner +=  '<img style="margin-left: 50px" src="%s"/>'%(self.url_banner)


		texto = u"""
					<html>
						<body>
							<div style="width: 980px; margin:0 auto;">

								<div style="padding: 20px 10px; background: #eaeaea;">
									<img src="%s"/>
									%s
								</div>

								<div style="padding: 20px 10px 40px 10px; 
			                            		border: 1px solid #eaeaea;
			                           			color: rgba(34, 34, 34, 0.76);
			                            		font-family: tahoma,'lucida grande',verdana,helvetica,arial,sans-serif;">

			                    	<div id="conteudo">	%s </div>

								</div>

								<div style="padding: 20px 10px; background: rgb(97,97,97); /* Old browsers */
			                                                	background: -moz-linear-gradient(top, rgba(97,97,97,1) 0%%, rgba(0,0,0,1) 100%%); /* FF3.6+ */
			                                                	background: -webkit-gradient(linear, left top, left bottom, color-stop(0%%,rgba(97,97,97,1)), color-stop(100%%,rgba(0,0,0,1))); /* Chrome,Safari4+ */
			                                                	background: -webkit-linear-gradient(top, rgba(97,97,97,1) 0%%,rgba(0,0,0,1) 100%%); /* Chrome10+,Safari5.1+ */
			                                                	background: -o-linear-gradient(top, rgba(97,97,97,1) 0%%,rgba(0,0,0,1) 100%%); /* Opera 11.10+ */
			                                                	background: -ms-linear-gradient(top, rgba(97,97,97,1) 0%%,rgba(0,0,0,1) 100%%); /* IE10+ */
			                                                	background: linear-gradient(to bottom, rgba(97,97,97,1) 0%%,rgba(0,0,0,1) 100%%); /* W3C */
			                                                	filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#616161', endColorstr='#000000',GradientType=0 ); /* IE6-9 */">
			               		
			               		<img src="%s">                                 		
							</div>
						</body>
					<html/>
				""" %(self.url_logo_topo,
				   	  banner,
				   	  self.conteudo,
				   	  self.url_logo_radape)
		
		return texto 

