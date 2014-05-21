from setuptools import setup, find_packages

setup(
    name = "django-mass-edit",
    version = "2.2",
    author = "David Burke",
    author_email = "david@burkesoftware.com",
    description = ("Make bulk changes in the Django admin interface"),
    license = "BSD",
    keywords = "django admin",
    url = "https://github.com/burke-software/django-mass-edit",
    packages=find_packages(),
    include_package_data=True,
    test_suite='setuptest.setuptest.SetupTestSuite',
    tests_require=(
        'django-setuptest',
        'south',
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=['django']
)
