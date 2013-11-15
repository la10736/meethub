from django.views import generic
from django.http import HttpResponseRedirect

from hubs.models import Hub
from events.models import Event

import logging

_ctx_index = 'hubs'
_tmpl_d = _ctx_index
_ctx_el = 'hub'

class IndexView(generic.ListView):
    model = Hub
    context_object_name = _ctx_index
    template_name = _tmpl_d + '/index.html'

class HubDispatchPanel(generic.DetailView):
    context_object_name = _ctx_el
    model = Hub
    template_name = _tmpl_d + '/hub_dispatch_panel.html'
    
    def post(self, request, *args, **kwargs):
        hub = self.get_object()
        try:
            selected_events = [Event.objects.get(pk=pk) for pk in request.POST['selected_events']]
        except (KeyError, Event.DoesNotExist):
            # Redisplay the poll voting form.
            logging.error("Niente Evento!!!")
        
        for d in hub.dispatcher_set.all():
            for e in selected_events:
                d.dispatch(e)
        
        return HttpResponseRedirect(request.path)