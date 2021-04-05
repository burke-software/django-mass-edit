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
2. In `settings.py`, add `massadmin` to `INSTALLED_APPS`
3. Add `path('admin/', include('massadmin.urls')),` to `urls.py` before `admin.site.urls` line 

## Optional
You may exclude some fields like this:

    ```python
    class PollAdmin(admin.ModelAdmin):
        massadmin_exclude = ['user', ]
    ```

You can also add or remove the "action" to models if you don't want it global. 
See [Django Docs on the subject](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#disabling-all-actions-for-a-particular-modeladmin)

## Custom AdminSite
    Django allows [customization of AdminSites](https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#customizing-adminsite)
    If you want to work with a custom AdminSite by passing the custom site to the view (it is also necessary to add the `mass_change_selected` action to the custom site):

        ```python
        from massadmin import mass_change_selected

        admin_site = MyCustomAdminSite(name='custom_admin')
        admin_site.add_action(mass_change_selected)

        url(r'^admin/', include(massadmin.urls), kwargs={'admin_site': admin_site}),
        ```

## Settings

### Enable Mass Edit for specific models

By default, all models registered in the admin will get `Mass Edit` action.

If you wish to disable this, add this to settings file:

``` python
MASSEDIT = {
    'ADD_ACTION_GLOBALLY': False,
}
``` 

Then, to add the mass edit action to specific models, use the provided mixin:
``` python
from massadmin.massadmin import MassEditMixin

class MyModelAdmin(MassEditMixin, admin.ModelAdmin):
    ...
``` 

### Session-based URLs

Django-mass-edit will keep IDs for selected objects in URL, e.g:
```
/admin/myapp/mymodel-masschange/1,2,3,4,5/
```

To avoid problems with too long URL when editing large number of objects, 
the list of objects will be stored in session and the URL will look like this:
```
/admin/myapp/mymodel-masschange/session-c81e728d9d4c2f636f067f89cc14862c/
```
(same length regardless of the number of selected objects).

The default threshold is 500 characters for the IDs in the URL, not counting 
anything before or after the the IDs.

This threshold can be changed in settings:

``` python
MASSEDIT = {
    'SESSION_BASED_URL_THRESHOLD': 10,
}
``` 

To always use the session-based URLs, simply put in value `0`.


# Hacking and pull requests

This project could use some love. It has few unit test and old code that could be refactored.
When you make a pull request - please include a unit test. 
If you want to take on improving the project let me know by opening an issue.

New maintainers welcome. I (bufke) will only be providing minimal support to keep the project running on modern versions of Django. Open an issue if you are interested.
