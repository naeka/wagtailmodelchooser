## Basic panel

Without any customization a basic panel can be generated like that:

```python
from wagtailmodelchooser.edit_handlers import register_chooser_for_model

ItemChooserPanel = register_chooser_for_model(Item)
```

The first argument of `register_chooser_for_model` must be a subclass of Django's `models.Model`.

Note that a `title` field is required on the model. It can be replaced with the `title_field` argument:

```python
ItemChooserPanel = register_chooser_for_model(Item, title_field='name')
```


## Basic customization

The `register_chooser_for_model` function accepts these arguments for more customizations:

* `widget_class` To use a custom widget class instead of the generated one.
* `widget_attrs` To set extra attrs to the generated widget class. Not used if `widget_class` is specified.
* `chooser_panel_base_class` To use a custom panel base class instead of the generated one.
* `chooser_view` To use a custom chooser view instead of the generated one.
* `chooser_view_attrs` To set extra attrs to the generated chooser view. Not used if `chooser_view` is specified.
* `chosen_view` To use a custom chosen view instead of the generated one.
* `chosen_view_attrs` To set extra attrs to the generated chosen view. Not used if `chosen_view` is specified.


## Advanced customization

To use totally custom classes, templates, the panel class can be directly built then registered like this:

```python
class EventChooserPanel(ModelChooserPanel):
    model = Event
    base_class = BaseEventChooserPanel
    chooser_view = EventChooserView
    chosen_view = EventChosenView

EventChooserPanel.register_with_wagtail()
```

The complete example is available in the test app.