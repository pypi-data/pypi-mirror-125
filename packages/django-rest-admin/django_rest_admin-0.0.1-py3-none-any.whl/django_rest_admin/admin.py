from django.contrib import admin
from .models import RouteExec,ComputedField
from django.contrib import admin
from django.utils.html import format_html

from .update_models import update_models
from .json_widget import JsonEditorWidget, CodeEditorWidget
from .model_field import JSONField, CodeField
# Register your models here.

@admin.action(description='使得参数修改起作用')
def make_published(modeladmin, request, queryset):
    #queryset.update(status='p')
    update_models(request)

class ComputedFieldAdmin(admin.TabularInline):
    model = ComputedField

class RouteExecAdmin(admin.ModelAdmin):
    inlines = [ComputedFieldAdmin, ]

    def button_link(self, obj):
        #if obj.re_type=='html':
        #    button_html = """<a class="changelink" href="/custom%s">打开</a>"""%(obj.route)
        #    button_html += """<a class="changelink" href="javascript:void(0)" onclick="update_amis_local_to_editor(%d)">编辑</a>""" % (obj.id)
        #elif obj.re_type=='table':
        button_html = """<a class="changelink" href="/rest_admin/api%s/">OpenApi</a>"""%(obj.route)
        #else:
        #    button_html="""nothing"""
        return format_html(button_html)

    button_link.short_description = "打开"

    list_display = ['id', 'route', 'button_link']
    actions = [make_published]
    formfield_overrides = {
            JSONField: {'widget': JsonEditorWidget},
            CodeField: {'widget': CodeEditorWidget},
        }

    class Media:
        css = {
            'all': ( 'django_rest_admin/jsoneditor.css',)
        }
        js = ('django_rest_admin/jsoneditor.js', 'django_rest_admin/jquery-3.6.0.min.js', 'django_rest_admin/add_button.js')


admin.site.register(RouteExec, RouteExecAdmin)
