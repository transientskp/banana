from django.contrib import admin
from .models import *

class TkpDbTabularInline(admin.TabularInline):
    using = 'banana'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def queryset(self, request):
        return super(TkpDbTabularInline, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        return super(TkpDbTabularInline, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        return super(TkpDbTabularInline, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


class TkpDbAdmin(admin.ModelAdmin):
    using = 'banana'

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
    list_display = ( 'id', 'runcat', 'siglevel', 'v_int', 'eta_int',
        'detection_level', 'trigger_xtrsrc', 'status', 't_start')

class ImagesInline(TkpDbTabularInline):
    model = Image
    list_display = ('id', 'ds', 'tau', 'band', 'stokes', 'tau_time',
        'freq_eff', 'freq_bw', 'taustart_ts')


class DatasetsAdmin(TkpDbAdmin):
    list_display = ('id', 'description', 'rerun', 'process_ts')
    #inlines = [ ImagesInline, ]

class ImagesAdmin(TkpDbAdmin):
    list_display = ('id', 'dataset', 'tau', 'band', 'stokes', 'tau_time',
        'freq_eff', 'freq_bw', 'taustart_ts', 'url')

admin.site.register(Transient, TransientsAdmin)
admin.site.register(Dataset, DatasetsAdmin)
admin.site.register(Image, ImagesAdmin)


