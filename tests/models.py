from django.db import models

from wagtailmodelchooser.views import ModelChooserView, ModelChosenView
from wagtailmodelchooser.edit_handlers import AdminModelChooser, ModelChooserPanel, register_chooser_for_model


class Event(models.Model):
    title = models.CharField(max_length=255)
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()


ItemChooserPanel = register_chooser_for_model(Item)


class EventChooserView(ModelChooserView):
    template_name = 'wagtaileventchooser/chooser/event_chooser.html'
    results_template_name = 'wagtaileventchooser/chooser/event_results.html'
    model = Event
    ordering = ['-starts_on', '-ends_on']
    title_field = 'title'
    model_chooser_url_name = 'event_chooser'
    model_chosen_url_name = 'event_chosen'


class EventChosenView(ModelChosenView):
    model = Event
    title_field = 'title'


class AdminEventChooser(AdminModelChooser):
    model = Event
    title_field = 'title'


class EventChooserPanel(ModelChooserPanel):
    object_type_name = 'event'
    model = Event
    widget_class = AdminEventChooser
    chooser_view = EventChooserView
    chosen_view = EventChosenView

EventChooserPanel.register_with_wagtail()
