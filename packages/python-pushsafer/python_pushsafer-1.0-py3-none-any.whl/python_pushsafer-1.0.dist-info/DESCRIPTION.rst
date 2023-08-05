.. image:: https://www.pushsafer.com/de/assets/logos/logo.png
    :alt: Pushsafer.com
    :width: 100%
    :align: center

``python-pushsafer`` aims at providing comprehensive Python bindings for the API
of the `Pushsafer Notification Service`_ as documented here__.

.. _Pushsafer Notification Service: https://www.pushsafer.com/ 
.. __: https://www.pushsafer.com/en/pushapi

Forked from and original created by: [Thibauth](https://github.com/Thibauth/python-pushover)

Installation
------------

Install from pip:

.. code-block::
   bash

   pip install python-pushsafer

or you can install it directly from GitHub_:

.. code-block::
    bash

    git clone https://github.com/appzer/python-pushsafer.git
    cd python-pushsafer
    pip install .

.. _GitHub: https://github.com/appzer/python-pushsafer

Overview
--------

.. code-block::
    python

    from pushsafer import Client

    client = Client("<privatekey>")
    resp = client.send_message("Message", "Hello", "323", "1", "4", "2", "https://www.pushsafer.com", "Open Pushsafer", "0", "2", "60", "600", "1", "", "", "")
    print(resp)


Params
------
.. code-block::
   python

   client.send_message(
                       "Message",
                       "Title",
                       "Device or Device Group ID",
                       "Icon",
                       "Sound",
                       "Vibration",
                       "URL",
                       "URL Title",
                       "Time2Live",
                       "Priority",
                       "Retry",
                       "Expire",
                       "Answer",
                       "Image 1",
                       "Image 2",
                       "Image 3")

API
---

You can access the full API documentation here__.

.. __: https://www.pushsafer.com/en/pushapi

Contributors
------------

* Kevin Siml <info@appzer.de>
* John Morris <2e0byo@gmail.com>

Changes
-------

1.0 (2021-10-25)
------------------

Fix bugs and completely rewrite.

0.4 (2018-08-19)
~~~~~~~~~~~~~~~~

add new pushsafer parameter priority, retry, expire, answer

0.3 (2017-11-28)
~~~~~~~~~~~~~~~~

ignore verifying the SSL certficate (trust self signed certificates)

0.2 (2017-02-12)
~~~~~~~~~~~~~~~~

Add new parameters (url, url title, time2live, image 1-3), minor bugfixes

0.1 (2016-09-13)
~~~~~~~~~~~~~~~~

Initial Release


