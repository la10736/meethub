from django.views import generic

from dispatchers.models import Dispatcher, DebugDispatcher, TestDispatcher

class IndexView(generic.ListView):
    model = Dispatcher
    context_object_name = 'dispatchers'
    template_name = 'dispatchers/index.html'
    
class DebugIndexView(IndexView):
    model = DebugDispatcher

class TestIndexView(IndexView):
    model = TestDispatcher

class _BaseDispatcherView(generic.DetailView):
    context_object_name = 'dispatcher'
    
class DebugDispatcherView(_BaseDispatcherView):
    model = DebugDispatcher
    template_name = 'dispatchers/debugdispatcher.html'

class TestDispatcherView(_BaseDispatcherView):
    model = TestDispatcher
    template_name = 'dispatchers/testdispatcher.html'
