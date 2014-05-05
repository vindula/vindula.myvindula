# -*- coding: utf-8 -*-
import pytz
from datetime import datetime
from datetime import timedelta

def delta2dict( delta ):
    """Accepts a delta, returns a dictionary of units"""
    delta = abs( delta )
    return {
        'ano'   : delta.days / 365 ,
        'dia'    : delta.days % 365 ,
        'hora'   : delta.seconds / 3600 ,
        'minuto' : (delta.seconds / 60) % 60 ,
        'segundo' : delta.seconds % 60 ,
        'microsegundo' : delta.microseconds
    }

def human(dt, precision=2, past_tense='{} atrás', future_tense=' {}'):
    """Accept a datetime or timedelta, return a human readable delta string"""
    delta = dt
    if type(dt) is not type(timedelta()):
        try:delta = datetime.now() - dt
        except:delta = datetime.now(pytz.timezone('America/Sao_Paulo')) - dt


    the_tense = past_tense
    if delta < timedelta(0):
        the_tense = future_tense

    d = delta2dict( delta )
    hlist = []
    count = 0
#     fist_s = ' a '
    units = ( 'ano', 'dia', 'hora', 'minuto', 'segundo')# REMOVIDO O MICROSEGUNDO 'microsegundo' )
    for unit in units:
        if count >= precision: break # met precision
        if d[ unit ] == 0: continue # skip 0's
        s = '' if d[ unit ] == 1 else 's' # handle plurals

        hlist.append( '%s %s%s' % ( d[unit], unit, s ) )
        count += 1

#    if hlist and hlist[0][-1] == 's':
#        fist_s = ' as '
#    else:
#        fist_s = ' a '
    
#     human_delta = fist_s + ' e '.join( hlist )
    human_delta = ' e '.join( hlist )
    return the_tense.format(human_delta)

