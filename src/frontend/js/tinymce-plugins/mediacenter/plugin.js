(function () {
  "use strict";

  var pluginManager = tinymce.util.Tools.resolve("tinymce.PluginManager");

  var global$1 = tinymce.util.Tools.resolve("tinymce.Env");

  const setup = (editor) => {
    const openMediacenter = () => {
      const el = document.createElement("div");
      document.body.append(el);
      window.preactRender(
        window.preactJSX(window.IntegreatSelectMediaDialog, {
          cancel: () => el.remove(),
          selectMedia: (file) => {
            el.remove();
            if(file.file_type.startsWith('image/')) {
                const linkEl = document.createElement('a');
                linkEl.href = file.path;
                linkEl.target = '_blank';
                const imageEl = document.createElement('img');
                imageEl.src = file.thumbnailPath;
                imageEl.alt = file.alt_text;
                linkEl.append(imageEl);
                editor.insertContent(linkEl.outerHTML);
            } else {
                const linkEl = document.createElement('a');
                linkEl.href = file.path;
                linkEl.innerText = file.name;
                editor.insertContent(linkEl.outerHTML);
            }
          },
        }),
        el
      );
    };

    editor.ui.registry.addButton("openmediacenter", {
      text: "Mediacenter",
      onAction: openMediacenter,
    });

    editor.ui.registry.addMenuItem("openmediacenter", {
      text: "Mediacenter...",
      icon: "image",
      onAction: openMediacenter,
    });
  };

  function Plugin() {
    pluginManager.add("mediacenter", function (editor) {
      setup(editor);
    });
  }

  Plugin();
})();
