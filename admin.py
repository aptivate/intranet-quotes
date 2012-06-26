import django.contrib.admin
import models

class QuoteAdmin(django.contrib.admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """

        form.save(commit=False)

        if request.POST.get('_promote'):
            from datetime import datetime
            obj.promoted = datetime.now()

        obj.save()
        form.save_m2m()        

django.contrib.admin.site.register(models.Quote, QuoteAdmin) 
