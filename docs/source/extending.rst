Extending Functionality
=======================

One of the core motivations behind Orb is to:

- make it easy for users to extend functionality by writing their own scripts and plugins
- make it easy for users to share plugins amongst themselves
- blur the line between users and developers

This entirely removes the dependency upon Orb's core development team, and follows the old adage of 'teaching someone how to fish'. Another good side-effect is the core development team can focus on delivering a high quality, stable core product while technical users can solve their own problems, and scratch their own itch.

Loading third-party modules
---------------------------

The currently recommended way of loading third-party modules is to extend `sys.path`. e.g

.. code:: python

    import sys
    sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
