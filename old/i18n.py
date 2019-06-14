#!/usr/bin/env python
#i18n.py
import glob

class I18n:
    def __init__(self, iso):
        self.load_languages()
        self.set_language(iso)

    def load_languages(self):
        self.languages = {}
        language_files = glob.glob("./i18n/*")
        for i in range(len(language_files)):
            lang = eval(open(language_files[i], 'r').read())
            iso = language_files[i].rsplit('/', 1)[1]
            self.languages[iso] = lang

    def set_language(self, iso):
        self.iso = iso
        self.dict = self.languages[iso]

    def trans(self, key):
        return self.dict[key]
