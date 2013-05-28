From Stanislaw Adaszewski's work (blog at http://algoholic.eu/django-mass-change-admin-site-extension/ ). I've fixed bugs and made changes to make it a production friendly drop-in Django app for bulk changes in Django's admin interface.

Check off what you want to edit in list view then choose mass edit from the actions menu. Image was taken using Grappelli

![Alt text](https://raw.github.com/burke-software/django-mass-edit/master/doc/screenshot9.png)

# Features
- Drop in app, works with all models in admin
- Doesn't allow users to edit unique and read only fields
- Attempts to detect and show users errors
- Database transactions ensure either all or no objects are changed

# Not implemented
- Custom forms
- No support for inlines. Original had this. I commented it out because I felt it was very buggy.
- Validation errors do not show up by the field they should

# Installation
easy_install django-mass-edit

In settings.py add massadmin to installed apps.

Add (r'^admin/', include("massadmin.urls")), to urls.py
