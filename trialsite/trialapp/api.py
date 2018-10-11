from .models import Trial, Enrollment

class TrialApi():
    def _create(self,title,address,city,country,pincode,discription,email,operator,organiser):
        trials = Trial(title=title,address=address,city=city,country=country,pincode=pincode,discription=discription,email=email,operator=operator,organiser=organiser)
        trials.save()
        return trials

    def _get(self,id):
        return Trial.objects.get(id=id)

    def _filter(self,id):
        return Trial.objects.filter(id=id)

    def _all(self):
        return Trial.objects.all


class EnrollmentApi():
    def _create(self, patient_username,email,trial_title,trial_organiser,trial_operator):
        enrollment = Enrollment(patient_username=patient_username,email=email,trial_title=trial_title,trial_organiser=trial_organiser,trial_operator=trial_operator)
        enrollment.save()
        return enrollment

    def _get(self, id):
        return Enrollment.objects.get(id=id)

    def _filter(self, id):
        return Enrollment.objects.filter(id=id)

    def _all(self):
        return Enrollment.objects.all