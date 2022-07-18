ansible-module-userdetect
=========================

{{ cli('ansible-doc userdetect') | literal }}

Development
===========

Test functionality
------------------

::

   /usr/local/src/ansible/hacking/test-module -m userdetect.py -a

Test documentation
------------------

::

   source /usr/local/src/ansible/hacking/env-setup
   /usr/local/src/ansible/test/sanity/validate-modules/validate-modules --arg-spec --warnings userdetect.py

Generate documentation
----------------------

::

   ansible-doc -M . userdetect
