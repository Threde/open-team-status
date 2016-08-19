function Editor(input, preview) {
    this.update = function () {
        preview.innerHTML = markdown.toHTML(input.value);
    };
    input.editor = this;
    input.onChange = this.update;
    input.onkeyup = this.update;
    this.update();
}
new Editor(
        document.getElementById('id_today'),
        document.getElementById('preview'));
