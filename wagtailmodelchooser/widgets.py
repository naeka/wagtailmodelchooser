from __future__ import absolute_import, unicode_literals

import json

from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.widgets import AdminChooser


class AdminModelChooser(AdminChooser):
    show_edit_link = False

    @property
    def choose_one_text(self):
        return _("Choose a %(model_verbose_name)s") % {'model_verbose_name': self.model._meta.verbose_name}

    @property
    def choose_another_text(self):
        return _("Choose another %(model_verbose_name)s") % {'model_verbose_name': self.model._meta.verbose_name}

    def render_html(self, name, value, attrs):
        instance, value = self.get_instance_and_id(self.model, value)
        original_field_html = super(AdminModelChooser, self).render_html(name, value, attrs)

        return render_to_string('wagtailmodelchooser/widgets/model_chooser.html', {
            'widget': self,
            'original_field_html': original_field_html,
            'attrs': attrs,
            'value': value,
            'instance': instance,
            'title_field': self.title_field,
        })

    def render_js_init(self, id_, name, value):
        return "createModelChooser({}, {});".format(json.dumps(id_), json.dumps(self.model.__name__))
