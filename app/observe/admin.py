from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from observe.models import Supernova, Observation, Exposure
# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse', ),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "sites":
            kwargs["initial"] = [Site.objects.get_current()]
        return super(FlatPageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ExposureInline(admin.TabularInline):
    model = Exposure

class SupernovaAdmin(admin.ModelAdmin):
    inlines = [
        ExposureInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }


class ObservationAdmin(admin.ModelAdmin):
    list_display = ['track_num','email','supernova','status']
    list_filter = ['status','supernova']

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


admin.site.register(Supernova, SupernovaAdmin)
admin.site.register(Observation, ObservationAdmin)

admin.site.site_header = 'Supernova Tracker admin'
admin.site.site_title = 'Supernova Tracker admin'
