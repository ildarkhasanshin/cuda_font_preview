import os
import tempfile
from cudatext import *

from cudax_lib import get_translation, safe_open_url
_ = get_translation(__file__)

import re
import string

plug_path = os.path.dirname(os.path.abspath(__file__))
plug_name = os.path.basename(plug_path)
dir_temp = os.path.join(tempfile.gettempdir(), plug_name)
fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'plugins.ini')
ini_section = plug_name.replace('cuda_', '')

class TplReplace(string.Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{) |
    (?P<named>[_a-z][_a-z0-9]*)\}\} |
    (?P<braced>[_a-z][_a-z0-9]*)\}\} |
    (?P<invalid>)
    )
    '''

class Command:
    opts_def = dict(
        file_exts = 'ttf,woff,eot,otf,ttc',
        tpl_fn = 'template.tpl',
        ft = 'The quick brown fox jumps over the lazy dog.',
        ft_loc = 'Съешь же ещё этих мягких французских булок, да выпей чаю.',
    )

    def __init__(self):
        self.opts = self.load_opts()
        if not os.path.isdir(dir_temp):
            os.mkdir(dir_temp)

    def on_open_pre(self, ed_self, fn):
        file_ext = self.get_fn_fe(fn)[1]
        if file_ext in self.opts['file_exts']:
            self.run(fn)
            return False

    def on_exit(self, ed_self):
        if os.path.isdir(dir_temp):
            for f in os.listdir(dir_temp):
                os.remove(os.path.join(dir_temp, f))
        os.rmdir(dir_temp)

    def load_opts(self):
        data = dict()
        for key in self.opts_def:
            data[key] = ini_read(fn_config, ini_section, key, self.opts_def[key])

        return data

    def save_opts(self):
        for key in self.opts:
            ini_write(fn_config, ini_section, key, self.opts[key])

    def config(self):
        self.save_opts()
        file_open(fn_config)
        lines = [ed.get_text_line(i) for i in range(ed.get_line_count())]
        try:
            index = lines.index('[' + ini_section + ']')
            ed.set_caret(0, index)
        except:
            pass

    def get_fn_fe(self, fn):
        fn = os.path.basename(fn)
        fe = os.path.splitext(fn)[1][1:].lower()
        fn_only = os.path.splitext(os.path.basename(fn))[0]
        return fn, fe, fn_only

    def run(self, fn):
        tpl = plug_path + os.sep + self.opts['tpl_fn']
        if os.path.isfile(tpl):
            with open(tpl, 'r', encoding='utf-8') as f:
                text = f.read()
            text = TplReplace(text).safe_substitute(
                font_title = self.get_fn_fe(fn)[0],
                font_name = self.get_fn_fe(fn)[2],
                font_file = fn,
                fish_text = self.opts['ft'],
                fish_text_loc = self.opts['ft_loc']
            )

            fn_temp = os.path.join(dir_temp, os.path.basename(fn) + '.html')
            with open(fn_temp, 'w', encoding='utf-8') as f:
                f.write(text)

            if os.path.isfile(fn_temp):
                msg_status(_('FontPreview: open file') + ' ' + fn_temp)
                safe_open_url('file://' + fn_temp)
            else:
                msg_status(_('FontPreview: cannot open file') + ' ' + fn_temp)
        else:
            msg_status(_('FontPreview: cannot open file') + ' ' + tpl)
