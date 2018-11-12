from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from .views import Trials
from .models import Trial
class TrialMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_request(self,request):
        print('Middleware process_request executed ')
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):

        trials = Trial.objects.all()

        for t in trials:
            if t.pincode == 333333:
                t.pincode = 222222
            elif t.pincode == 222222:
                t.pincode = 111111
            else:
                t.pincode = 333333
            t.save()
        return None


    def process_template_reponse(self, request, response):
        response.context_data ={}
        response.template_name = 'trialapp/investigator_dashboard.html'
        print(response)
        return response


    def process_response(self, request, response):
        print("Another Middleware process_response executed")
        return response