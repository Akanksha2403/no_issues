tinymce.init({
    // selector to be only used on the textarea with the class 'tinymce'
    selector: '.tinymce',
    plugins: "a11ychecker advcode advlist advtable anchor autocorrect autolink autoresize autosave casechange charmap checklist code codesample directionality editimage emoticons export footnotes formatpainter fullscreen help image importcss inlinecss insertdatetime link linkchecker lists media mediaembed mentions mergetags nonbreaking pagebreak pageembed permanentpen powerpaste preview quickbars save searchreplace table tableofcontents template tinycomments tinydrive tinymcespellchecker typography visualblocks visualchars wordcount",
    toolbar: 'undo redo | bold italic underline strikethrough | subscript superscript | fontsizeselect fontselect forecolor backcolor | formatselect | bullist numlist outdent indent | alignleft aligncenter alignright alignjustify | removeformat | link unlink anchor | image table hr | code | blockquote | charmap | fullscreen',
    autoresize_bottom_margin: 120,
    branding: false,
    promotion: false, 
    autohide: false
});