[![Build Status](https://travis-ci.org/burke-software/django-mass-edit.svg?branch=master)](https://travis-ci.org/burke-software/django-mass-edit)
[![Coverage Status](https://coveralls.io/repos/burke-software/django-mass-edit/badge.svg?branch=master&service=github)](https://coveralls.io/github/burke-software/django-mass-edit?branch=master)

From Stanislaw Adaszewski's [blog](http://algoholic.eu/django-mass-change-admin-site-extension/ ). 
I've fixed bugs and made changes to make it a production friendly drop-in Django app for bulk changes in Django's 
admin interface.

Check off what you want to edit in list view then choose mass edit from the actions menu. 
Image was taken using Grappelli

![Alt text](https://raw.github.com/burke-software/django-mass-edit/master/doc/screenshot9.png)

# Features
- Drop in app, works with all models in admin
- Doesn't allow users to edit unique and read only fields
- Attempts to detect and show users errors
- Database transactions ensure either all or no objects are changed

# Not implemented
- No support for inlines. Original had this. I commented it out because I felt it was very buggy.
- Validation errors do not show up by the field they should

# Installation

1. `pip install django-mass-edit`
2. In settings.py, add `'massadmin'` to installed apps
3. In urls.py, add:
```
    from massadmin import urls as massadmin_urls
    from massadmin import mass_change_selected
    admin.site.add_action(mass_change_selected)
```
    
   and add to urls:
```
    url(r'', include(massadmin_urls)),
``` 
## Optional
You may exclude some fields like this:

    class PollAdmin(admin.ModelAdmin):
        massadmin_exclude = ['user', ]

You can also add or remove the "action" to models if you don't want it global. 
See [Django Docs on the subject](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#disabling-all-actions-for-a-particular-modeladmin)

# Hacking and pull requests

This project could use some love. It has few unit test and old code that could be refactored.
When you make a pull request - please include a unit test. 
If you want to take on improving the project let me know by opening an issue.

New maintainers welcome. I (bufke) will only be providing minimal support to keep the project running on modern versions of Django. Open an issue if you are interested.

# Changelog

3.0 - Use sessions instead of GET params for id passing. Started using git tags for nicer release tracking.

2.6 - Added Django 1.10 support
