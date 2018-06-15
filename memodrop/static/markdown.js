function markdownEditor(parameters) {
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
    parameters.element.attr("required", false);
    return simplemde;
}
