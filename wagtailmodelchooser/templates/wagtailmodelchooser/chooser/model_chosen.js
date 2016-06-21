function(modal) {
    modal.respond('modelChosen', {{ model_json|safe }});
    modal.close();
}