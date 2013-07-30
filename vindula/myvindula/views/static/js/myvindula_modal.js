$j = jQuery.noConflict();

function  createElement(name) {
    return $(document.createElement(name));
}

$j(document).ready(function(){
    
    $('a.profile-link').hover(function(ev){
        var $el = $(this);
        
        if($el.next().hasClass('profile-modal')){
            $el.next().show();
        }else{
            var container = createElement('div').attr({'class': 'profile-modal'});
            $el.after(container);
        }
    });
 });
 
 /*
        <div class="box-updates box-notify box-hidden active">
            <div class="seta-box">
                <img src="http://192.168.0.113/++resource++vindula.tile/images/seta-box.png"></div>
            <div class="updates-header clear">
              <div class="left"><strong>Notificações</strong></div>
              <!--div class="right"><a href="#">Configurações</a></div-->
            </div>
            <div class="scrollable-area updates-content">

              <ul class="letters no-bullet" id="itens"><!-- Boco de codigo para novas notificação --><li class="container-item unread hide" id="new-list-notify">
                      <a href="" class="link">
                          <div class="clear">
                              <div class="circle-mark"> </div>
                              <img class="left photo" width="50" height="50" src=""><div class="left info-updates">
                                  <div>
                                      <strong class="name"></strong>
                                      <span class="text"></span>
                                      <span>agora</span>
                                  </div>
                              </div>
                          </div>
                      </a>
                  </li>

                  
                      <li class="container-item unread">

                        

                          <a>
                              <div class="clear">
                                  <div class="circle-mark">
                                  </div>
                                  <img class="left" width="50" height="50" src="http://192.168.0.113/vindula-api/myvindula/user-picture/photograph/catarinafernandes/True"><div class="left info-updates">
                                      <div>
                                          <strong>Catarina Fernandes</strong>
                                          <span> seguiu </span>
                                          o conteudo

                                          <span> a 10 dias e 19 horas atrás</span>
                                      </div>
                                  </div>
                              </div>
                          </a>
                        
                      </li>
                  
                  
                      <li class="container-item unread">

                        

                          <a href="http://192.168.0.113/comunicacao/blog-corporativo/brasileiros-pagam-mais-que-o-dobro-que-americanos-pelos-novos-macs">
                              <div class="clear">
                                  <div class="circle-mark">
                                  </div>
                                  <img class="left" width="50" height="50" src="http://192.168.0.113/vindula-api/myvindula/user-picture/photograph/catarinafernandes/True"><div class="left info-updates">
                                      <div>
                                          <strong>Catarina Fernandes</strong>
                                          <span> seguiu </span>
                                          o conteudo

                                          <span> a 10 dias e 22 horas atrás</span>
                                      </div>
                                  </div>
                              </div>
                          </a>
                        
                      </li>
                  
                  
                      <li class="container-item unread">

                        

                          <a href="http://192.168.0.113/comunicacao/blog-corporativo/brasileiros-pagam-mais-que-o-dobro-que-americanos-pelos-novos-macs">
                              <div class="clear">
                                  <div class="circle-mark">
                                  </div>
                                  <img class="left" width="50" height="50" src="http://192.168.0.113/vindula-api/myvindula/user-picture/photograph/catarinafernandes/True"><div class="left info-updates">
                                      <div>
                                          <strong>Catarina Fernandes</strong>
                                          <span> curtiu </span>
                                          o conteudo

                                          <span> a 10 dias e 22 horas atrás</span>
                                      </div>
                                  </div>
                              </div>
                          </a>
                        
                      </li>
                  
                  
                      <li class="container-item unread">

                        

                          <a href="http://192.168.0.113/comunicacao/blog-corporativo/inauguracao-da-intranet">
                              <div class="clear">
                                  <div class="circle-mark">
                                  </div>
                                  <img class="left" width="50" height="50" src="http://192.168.0.113/vindula-api/myvindula/user-picture/photograph/catarinafernandes/True"><div class="left info-updates">
                                      <div>
                                          <strong>Catarina Fernandes</strong>
                                          <span> curtiu </span>
                                          o conteudo

                                          <span> a 10 dias e 22 horas atrás</span>
                                      </div>
                                  </div>
                              </div>
                          </a>
                        
                      </li>
                  
                  
                      <li class="container-item unread">

                        

                          <a href="http://192.168.0.113/comunicacao/blog-corporativo/inauguracao-da-intranet">
                              <div class="clear">
                                  <div class="circle-mark">
                                  </div>
                                  <img class="left" width="50" height="50" src="http://192.168.0.113/vindula-api/myvindula/user-picture/photograph/catarinafernandes/True"><div class="left info-updates">
                                      <div>
                                          <strong>Catarina Fernandes</strong>
                                          <span> seguiu </span>
                                          o conteudo

                                          <span> a 10 dias e 22 horas atrás</span>
                                      </div>
                                  </div>
                              </div>
                          </a>
                        
                      </li>
                  
              </ul></div>
            <div class="updates-footer clear">
              <strong><a class="profile-link" href="http://192.168.0.113/myvindulalistuser?session=notification">Ver todas</a></strong>
            </div>
        </div>
*/