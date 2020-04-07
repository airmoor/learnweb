from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    #add atstic/css/admin.css to the admin
    return format_html('<link rel="stylesheet" href="{}">', static("css/admin.css"))

@hooks.register('construct_main_menu')
def hide_reports(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name != 'reports']
