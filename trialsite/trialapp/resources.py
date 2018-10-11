from import_export import resources
from .models import Trial

class TrialResource(resources.ModelResource):
    class Meta:
        model = Trial