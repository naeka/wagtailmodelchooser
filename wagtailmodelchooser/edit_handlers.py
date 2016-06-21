from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.core import urlresolvers
from django.db import models
from django.utils.html import format_html, format_html_join

from wagtail.wagtailadmin.edit_handlers import BaseChooserPanel
from wagtail.wagtailcore import hooks

from .widgets import AdminModelChooser
from .views import ModelChooserView, ModelChosenView


class BaseModelChooserPanel(BaseChooserPanel):
    @classmethod
    def widget_overrides(cls):
        return {cls.field_name: cls.widget_class}


class ModelChooserPanel(object):
    def __init__(self, field_name):
        self.field_name = field_name

    def bind_to_model(self, model):
        return type(str('_{}ChooserPanel'.format(model._meta.object_name)), (self.base_class,), {
            'model': model,
            'field_name': self.field_name,
        })

    @classmethod
    def register_with_wagtail(cls):
        @hooks.register('register_admin_urls')
        def register_admin_urls():
            return cls.get_admin_urls_for_registration()

        @hooks.register('insert_editor_js')
        def insert_editor_js():
            return cls.get_editor_js_for_registration()

    @classmethod
    def get_admin_urls_for_registration(cls):
        return (
            url(r'^{}/chooser/$'.format(cls.model._meta.model_name), cls.chooser_view.as_view(),
                name='{}_chooser'.format(cls.model._meta.model_name)),
            url(r'^{}/chooser/(?P<pk>\d+)/$'.format(cls.model._meta.model_name), cls.chosen_view.as_view(),
                name='{}_chosen'.format(cls.model._meta.model_name)),
        )

    @classmethod
    def get_editor_js_for_registration(cls):
        js_files = cls.get_editor_js_files()

        js_includes = format_html_join(
            '\n', '<script src="{0}{1}"></script>',
            ((settings.STATIC_URL, filename) for filename in js_files)
        )
        return js_includes + format_html(
            """
            <script>
                window.chooserUrls.{0}Chooser = '{1}';
            </script>
            """,
            cls.model._meta.object_name,
            urlresolvers.reverse('{}_chooser'.format(cls.model._meta.model_name))
        )

    @classmethod
    def get_editor_js_files(cls):
        return [
            'wagtailmodelchooser/js/model-chooser.js',
        ]


def register_chooser_for_model(
        model, widget_class=None, widget_attrs={}, chooser_panel_base_class=None, chooser_view=None,
        chooser_view_attrs={}, chosen_view=None, chosen_view_attrs={}, title_field='title'):

    # Ensure the model is well defined
    assert issubclass(model, models.Model), "model must be a subclass of Django's models.Model"

    # Build the chooser panel class
    class_name = model._meta.object_name

    # Check or build the widget class
    if widget_class:
        if not getattr(widget_class, 'model', None) == model:
            raise AssertionError("Incorrect model attribute for {}: '{}.{}' is expected".format(
                widget_class.__name__, model.__module__, model.__name__))
    else:
        defaults = {
            'model': model,
            'title_field': title_field,
        }
        defaults.update(**widget_attrs)
        widget_class = type(str('Admin{}Chooser'.format(class_name)), (AdminModelChooser,), defaults)

    # Check or build the chooser panel base class
    if chooser_panel_base_class:
        assert issubclass(chooser_panel_base_class, BaseModelChooserPanel), \
            "chooser_panel_base_class must inherit from 'BaseModelChooserPanel'"
        assert hasattr(chooser_panel_base_class, 'object_type_name'), \
            "chooser_panel_base_class must define 'object_type_name'"
        assert hasattr(chooser_panel_base_class, 'widget_class'), \
            "chooser_panel_base_class must define 'widget_class'"
    else:
        chooser_panel_base_class = type(str('Base{}ChooserPanel'.format(class_name)), (BaseModelChooserPanel,), {
            'object_type_name': model._meta.model_name,
            'widget_class': widget_class,
        })

    # Check or build the chooser view
    if chooser_view:
        if not getattr(chooser_view, 'model', None) == model:
            raise AssertionError("Incorrect model attribute for {}: '{}.{}' is expected".format(
                chooser_view.__name__, model.__module__, model.__name__))
        assert hasattr(chooser_view, 'title_field'), "chooser_view must define 'title_field'"
        assert hasattr(chooser_view, 'model_chooser_url_name'), "chooser_view must define 'model_chooser_url_name'"
        assert hasattr(chooser_view, 'model_chosen_url_name'), "chooser_view must define 'model_chosen_url_name'"
    else:
        defaults = {
            'model': model,
            'ordering': ['-pk'],
            'title_field': title_field,
            'model_chooser_url_name': '{}_chooser'.format(model._meta.model_name),
            'model_chosen_url_name': '{}_chosen'.format(model._meta.model_name),
        }
        defaults.update(**chooser_view_attrs)
        chooser_view = type(str('{}ChooserView'.format(class_name)), (ModelChooserView,), defaults)

    # Check or build the chosen view
    if chosen_view:
        if not getattr(chosen_view, 'model', None) == model:
            raise AssertionError("Incorrect model attribute for {}: '{}.{}' is expected".format(
                chosen_view.__name__, model.__module__, model.__name__))
        assert hasattr(chosen_view, 'title_field'), "chooser_view must define 'title_field'"
    else:
        defaults = {'model': model, 'title_field': title_field}
        defaults.update(**chosen_view_attrs)
        chosen_view = type(str('{}ChosenView'.format(class_name)), (ModelChosenView,), defaults)

    # Build the chooser panel class
    chooser_panel_class = type(str('{}ChooserPanel'.format(class_name)), (ModelChooserPanel,), {
        'model': model,
        'base_class': chooser_panel_base_class,
        'chooser_view': chooser_view,
        'chosen_view': chosen_view,
    })

    # Register with wagtail hooks
    chooser_panel_class.register_with_wagtail()

    return chooser_panel_class
