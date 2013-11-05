from setuptools import setup, find_packages

setup(
    name = "django-mass-edit",
    version = "2.0",
    author = "David Burke",
    author_email = "david@burkesoftware.com",
    description = ("Make bulk changes in the Django admin interface"),
    license = "BSD",
    keywords = "django admin",
    url = "http://code.google.com/p/django-mass-edit/",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
)
