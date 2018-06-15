$(document).ready(function() {
    markdownEditor({element: $("#id_question"), autofocus: true});
    markdownEditor({element: $("#id_hint")});
    markdownEditor({element: $("#id_answer")});
});
