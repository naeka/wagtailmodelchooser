from __future__ import absolute_import, unicode_literals

import json

from django.views.generic import DetailView, ListView
from django.shortcuts import render

from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailadmin.forms import SearchForm
from wagtail.utils.pagination import paginate


def get_model_data(cls, instance, title_field):
    return {
        'id': instance.id,
        'title': getattr(instance, title_field),
    }


class ModelChooserView(ListView):
    template_name = 'wagtailmodelchooser/chooser/model_chooser.html'
    results_template_name = 'wagtailmodelchooser/chooser/model_results.html'
    js_handler_template_name = 'wagtailmodelchooser/chooser/model_chooser.js'
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super(ModelChooserView, self).get_context_data(**kwargs)
        context.update(
            model_chooser_url_name=self.model_chooser_url_name, model_chosen_url_name=self.model_chosen_url_name,
            is_searching=self.is_searching, model_verbose_name=self.model._meta.verbose_name,
            model_verbose_name_plural=self.model._meta.verbose_name_plural
        )
        return context

    def get(self, request, *args, **kwargs):
        self.is_searching = False
        self.object_list = self.get_queryset()

        if 'q' in self.request.GET or 'p' in self.request.GET:
            searchform = self.form_class(self.request.GET)
            if searchform.is_valid():
                self.is_searching = True
                self.object_list = self.object_list.filter(**{
                    '{}__icontains'.format(self.title_field): searchform.cleaned_data.get('q')
                })

            paginator, self.object_list = paginate(request, self.object_list, per_page=10)
            context = self.get_context_data(searchform=searchform, query_string=searchform.cleaned_data.get('q'))
            return render(request, self.results_template_name, context)
        else:
            searchform = self.form_class()

        paginator, self.object_list = paginate(request, self.object_list, per_page=10)
        context = self.get_context_data(searchform=searchform)

        return render_modal_workflow(request, self.template_name, self.js_handler_template_name, context)


class ModelChosenView(DetailView):
    model_data_extractor = get_model_data

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render_modal_workflow(
            request, None, 'wagtailmodelchooser/chooser/model_chosen.js',
            {'model_json': json.dumps(self.model_data_extractor(self.object, self.title_field))}
        )
