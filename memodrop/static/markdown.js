function markdownEditor(parameters) {
    if(!getUserGUISettingsAttribute("enable_markdown_editor")) return;
    var simplemde = new SimpleMDE({
        element: parameters.element[0],
        autofocus: parameters.autofocus,
        forceSync: true,
        autoDownloadFontAwesome: false,
        spellChecker: false,
        status: false,
        renderingConfig: {
            singleLineBreaks: false
        },
        toolbar: [
            "bold",
            "italic",
            "strikethrough",
            "|",
            "quote",
            "unordered-list",
            "ordered-list",
            "|",
            "link",
            "image",
            "table",
            "code",
            "|",
            "preview"
        ]
    });
    try {
        parameters.element.attr("required", false);
    } catch(TypeError) {
        console.log("Element does not have a \"required\" attribute");
    }
    return simplemde;
}
