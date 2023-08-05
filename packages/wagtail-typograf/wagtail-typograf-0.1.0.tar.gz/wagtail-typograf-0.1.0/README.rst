wagtail-typograf
----------------

A plugin to add `typus <https://github.com/byashimov/typus>`_ functionality to wagtail rich text editor (draftail).

Demo
====

.. image:: https://raw.githubusercontent.com/truetug/wagtail-typograf/master/demo.gif
    :width: 400
    :alt: Demo

Installation
============

* Install with pip 

::

    pip install wagtail-typograf

* Add app name to your list of installed apps
  
::

    INSTALLED_APPS = [
        ...
        "wagtail_typograf",
    ]
    
* Add typograf url to your urlpatterns (for now "/api/typograf/" is strongly hardcoded in js)

::

    urlpatterns = [
      ...
      path('api/', include('wagtail_typograf.urls')),
      ...
    ]


* If you use limit number of features in RichTextBlock, don't forget to add ``typograf`` to its list

::
    
    text_block = RichTextBlock(
        features=[
            "bold", "italic", "ol", "ul", "hr", 
            "link", "document-link", "typograf",
        ],
        ...
    )

Usage
=====

Write or paste text content, push the ¶-button.
