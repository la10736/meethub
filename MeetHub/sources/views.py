from django.views import generic
from django.views.generic.edit import FormView

from sources.models import Source, DebugSource, TestSource
from sources.form import DebugForm

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

class _BaseSourceView(generic.DetailView):
    context_object_name = _ctx_el

class DebugSourceView(_BaseSourceView):
    model = DebugSource
    template_name = _tmpl_d + '/debugsource.html'
    form_class = DebugForm
    
    def get_context_data(self, **kwargs):
        context = super(DebugSourceView, self).get_context_data(**kwargs)
        context['form'] = DebugForm
        return context
    
class DebugSourcePost(FormView):
    #success_url = 'go/here/if/all/works'
    form_class = DebugForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_event(self.get_object())
        return super(DebugSourceView, self).form_valid(form)

class TestSourceView(_BaseSourceView):
    model = TestSource
    template_name = _tmpl_d + '/testsource.html'
