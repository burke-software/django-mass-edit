# Changelog

3.5.1 (unreleased)
------------------

* Fixed work with string primary keys that have special characters

3.5.0 (22-08-2023)
------------------

* Updates for Django up to 4.2
* ``mass_change_view()`` should also call ``get_queryset()`` from ``admin_obj`` (#111)
* ``mass_edit_view()`` should call ``get_form()`` on ``admin_obj`` (#112)
* Use the admin obj's hook methods (``get_fieldsets``, etc) instead of the MassAdmin's own (#103)

3.4.1 (17-12-2021)
------------------

* Fix crashes for models that have `change_form_template` set

3.4.0 (17-12-2021)
------------------

* Supports Django 2.1 and newer
* Add support for Django up to 4.0

3.3.0 (04-10-2021)
------------------

* Remove Django 1.8 support
* Add context variables from site's `each_context()`
* Russian translation
* CSS compatibility with django-filter
* optionally disable global action
* provide mixin
* Add Django 2.2 and 3.0 support

3.2.0 (30-08-2018)
------------------

* Add Django 2.1 support
* Allow massadmin to be used with a custom AdminSite

3.1 (09-01-2018)
------------------

* Added Django 2.0 support.

3.0 (16-03-2017)
------------------

* Use sessions instead of GET params for id passing. Started using git tags for nicer release tracking.

2.6 ()
------------------

* Added Django 1.10 support
