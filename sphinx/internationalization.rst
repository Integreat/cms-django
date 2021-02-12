***************************
Internationalization (i18n)
***************************

For more detailed information, have a look at the official Django documentation on :doc:`topics/i18n/index`.


Hardcoded Strings
=================

Whenever you use hardcoded strings, use english text and encapsulate it with a translation function.

Models
------

::

    from django.utils.translation import ugettext_lazy as _

    string = _('Your string')

Views
-----

::

    from django.utils.translation import ugettext as _

    string = _('Your string')

Templates
---------

::

    {% trans 'Your string' %}


Translation File
================

.. highlight:: bash

After you finished your changes to the code base, run the following command::

    cd src/cms
    pipenv run integreat-cms-cli makemessages -l de

Then, open the file :github-source:`src/cms/locale/de/LC_MESSAGES/django.po` and fill in the german translations::

    msgid "Your string"
    msgstr "Deine Zeichenkette"


Compilation
===========

To actually see the translated strings in the backend UI, compile the django.po file as follows::

    cd src/cms
    pipenv run integreat-cms-cli compilemessages


Developer Tools
===============

To do ``makemessages`` and ``compilemessages`` in one step, use :github-source:`dev-tools/translate.sh`::

    ./dev-tools/translate.sh

If you run into merge/rebase conflicts inside the translation file, use :github-source:`dev-tools/resolve_translation_conflicts.sh`::

    ./dev-tools/resolve_translation_conflicts.sh

If you want to check, whether your translations is up-to-date or if there are any actions required, run :github-source:`dev-tools/check_translations.sh`::

    ./dev-tools/check_translations.sh
