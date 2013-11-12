from django.views import generic

from events.models import Event

_ctx_index = 'events'
_tmpl_d = _ctx_index
_ctx_el = 'event'

class IndexView(generic.ListView):
    model = Event
    context_object_name = _ctx_index
    template_name = _tmpl_d + '/index.html'

class EventView(generic.DetailView):
    context_object_name = _ctx_el
    model = Event
    template_name = _tmpl_d + '/event.html'
