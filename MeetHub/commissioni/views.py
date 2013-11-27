from django.views import generic

from commissioni.models import CdZ

_ctx_index = 'consigli'
_tmpl_d = _ctx_index
_ctx_el = 'CdZ'

class CdZIndexView(generic.ListView):
    model = CdZ
    context_object_name = _ctx_index
    template_name = _tmpl_d + '/index.html'

def _g(r,c,t):
    return r.POST[c+"_"+t]

def _gg(r,c,*args):
    return (_g(r,c,x) for x in args) 

class CdZView(generic.DetailView):
    context_object_name = _ctx_el
    model = CdZ
    template_name = _tmpl_d + '/cdz.html'
    
    def get_context_data(self, **kwargs):
        context = super(CdZView, self).get_context_data(**kwargs)
        cc = CdZ.get_prossime_commisioni_from_url(self)
        context['commissioni'] = cc
        return context

    def post(self, request, *args, **kwargs):
        cdz = self.get_object()
        r = request
        commissioni = r.POST.getlist('commissioni')
        for c in commissioni:
            cdz._nuova_commissione(*_gg(r,c,'nr', 'nome', 'url', 'start_date', 'end_date', 'congiunta'))
        
        return HttpResponseRedirect(request.path)