from django.views import generic

from sources.models import Source, DebugSource, TestSource

_ctx_index = 'sources'
_tmpl_d = _ctx_index
_ctx_el = 'source'

class IndexView(generic.ListView):
    model = Source
    context_object_name = _ctx_index
    template_name = _tmpl_d + '/index.html'
    
class DebugIndexView(IndexView):
    model = DebugSource

class TestIndexView(IndexView):
    model = TestSource

class _BaseDispatcherView(generic.DetailView):
    context_object_name = _ctx_el
    
class DebugDispatcherView(_BaseDispatcherView):
    model = DebugSource
    template_name = _tmpl_d + '/debugsource.html'

class TestDispatcherView(_BaseDispatcherView):
    model = TestSource
    template_name = _tmpl_d + '/testsource.html'
