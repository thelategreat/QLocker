from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.template import Context, RequestContext
import functions

class editorView(TemplateView):
    template_name = 'editor.html'

    def get_context_data(self, **kwargs):
        equationString = "(cos(<x>^2)/<y>)*60"
        latexString = functions.convertStringToEquation(equationString)
        ctx = {'latexString':latexString}
        return ctx
        
        
class ajaxEquationView(TemplateView, FormMixin):
    template_name = "ajaxEquation.html"

    #def get(self, request, *args, **kwargs):
        #print request.GET.get('test', 'no')
        #context = {'a':'1'} # compute what you want to pass to the template
        
        #return super(ajaxEquationView, self).get(self, request, *args, **kwargs)
        ##return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        #context = super(ajaxEquationView, self).get(self, request, *args, **kwargs)
        print "hi"
        equationString = self.request.GET.get('e', '')
        #equationString = "(cos(<x>^2)/<y>)*60"
        latexString = functions.convertStringToEquation(equationString)
        #print context
        ctx = {'latexString':latexString}
        return ctx