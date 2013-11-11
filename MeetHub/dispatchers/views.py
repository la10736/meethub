from django.views import generic

from dispatchers.models import Dispatcher, DebugDispatcher, TestDispatcher

_ctx_index = 'dispatchers'
_tmpl_d = _ctx_index
_ctx_el = 'dispatcher'

class IndexView(generic.ListView):
    model = Dispatcher
    context_object_name = _ctx_index
    template_name = _tmpl_d + '/index.html'
    
class DebugIndexView(IndexView):
    model = DebugDispatcher

class TestIndexView(IndexView):
    model = TestDispatcher

class _BaseDispatcherView(generic.DetailView):
    context_object_name = _ctx_el
    
class DebugDispatcherView(_BaseDispatcherView):
    model = DebugDispatcher
    template_name = _tmpl_d + '/debugdispatcher.html'

class TestDispatcherView(_BaseDispatcherView):
    model = TestDispatcher
    template_name = _tmpl_d + '/testdispatcher.html'
