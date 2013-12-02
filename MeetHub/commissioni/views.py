from django.views import generic

from commissioni.models import CdZ, Commissione
from django.http.response import HttpResponseRedirect
from django.utils import timezone

_ctx_index = 'commissioni'
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
        cc = self.get_object().get_prossime_commisioni_from_url()
        context['commissione_obsolete'] = [ c for c in cc if c["old"]]
        context['commissioni_new'] = [c for c in cc if not c.has_key("ref") and not c["old"]]
        context['commissioni_modif'] = [c for c in cc if c.has_key("changed")]
        context['commissioni_old'] = [c for c in cc if c.has_key("ref") and not c.has_key("changed")]
        refs = [c["ref"] for c in cc if c.has_key("ref")]
        now = timezone.now()
        context['commissioni_orfane'] = [c for c in Commissione.objects.filter(start_date__gte=now) if not c in refs]
        context['commissioni_in_corso'] = Commissione.objects.filter(start_date__lte=now,end_date__gt=now)
        
        return context

    def post(self, request, *args, **kwargs):
        cdz = self.get_object()
        r = request
        creare = r.POST.getlist('creare')
        for c in creare:
            cdz._nuova_commissione(*_gg(r,"creare_"+c,'nr', 'nome', 'url', 'data', 'inizio', 'fine', 'congiunta'))
        
        return HttpResponseRedirect(request.path)