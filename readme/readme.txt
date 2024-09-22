Plugin for CudaText.
Shows html-preview of font-file (default-ext: ttf, woff, eot, otf, ttc) in WebBrowser.

How to use
----------
1) Open font-file in CudaText
2) In CudaText-dialog "File is maybe not text" press "Cancel"-button or ESC-key.
3) Switch to default-WebBrowser where opened new tab with html-preview of font.

Configuration
-------------
Menu item "Options / Settings-plugins / Font Preview / Config".

Options in the settings/plugins.ini file, in [font_preview], are:
- "file_exts": file-extensions that the plugin will open
- "tpl_fn": file-template for html-preview
- "ft": fish-text
- "ft_loc": local fish-text

Author:
  ildar r. khasanshin (@ildarkhasanshin at GitHub)
License: MIT