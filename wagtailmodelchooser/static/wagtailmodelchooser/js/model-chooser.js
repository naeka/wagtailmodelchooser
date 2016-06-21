function createModelChooser(id, modelName) {
    var chooserElement = $('#' + id + '-chooser');
    var modelTitle = chooserElement.find('.title');
    var input = $('#' + id);

    $('.action-choose', chooserElement).click(function() {
        ModalWorkflow({
            url: window.chooserUrls[modelName + "Chooser"],
            responses: {
                modelChosen: function(docData) {
                    input.val(docData.id);
                    modelTitle.text(docData.title);
                    chooserElement.removeClass('blank');
                }
            }
        });
    });

    $('.action-clear', chooserElement).click(function() {
        input.val('');
        chooserElement.addClass('blank');
    });
}