from django.contrib import admin
from .models import *

class TkpDbAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'tkpdb'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(TkpDbAdmin, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(TkpDbAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(TkpDbAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class TransientsAdmin(TkpDbAdmin):
    pass

class DatasetsAdmin(TkpDbAdmin):
    list_display = ('dsid', 'rerun', 'dstype', 'process_ts', 'dsinname',
            'dsoutname', 'description')

admin.site.register(Transients, TransientsAdmin)
admin.site.register(Datasets, DatasetsAdmin)

