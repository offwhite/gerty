#!/usr/bin/env python

import i18n

I18n = i18n.I18n('en')

print I18n.trans('login')

I18n.set_language('fr')

print I18n.trans('login')
