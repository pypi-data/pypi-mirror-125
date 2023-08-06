Introduction
============

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython framebuf based driver for Pimoroni's Unicorn HAT HD.
This driver supports the `adafruit_framebuf interface <https://circuitpython.readthedocs.io/projects/framebuf/en/latest/>`__ via composition instead of inheritance.

.. image:: ./images/unicornhathd_rainbow.png
   :alt: Pimoroni Unicorn HAT HD on breadboard
   :scale: 50%
   :align: center


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Adafruit framebuf <https://github.com/adafruit/Adafruit_CircuitPython_framebuf>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-unicornhathd/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-unicornhathd

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-unicornhathd

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install circuitpython-unicornhathd



Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install unicornhathd

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

  import board
  import digitalio
  from unicornhathd import UnicornHATHD

  # TODO: Change this pin to match your wiring
  chip_select_pin = digitalio.DigitalInOut(board.D0)
  chip_select_pin.direction = digitalio.Direction.OUTPUT
  chip_select_pin.value = True

  display = UnicornHATHD(board.SPI(), chip_select_pin)

  # Turn on all of the blue LEDs
  display.fill(127)
  display.show()

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/NathanY3G/CircuitPython_Unicorn_HAT_HD/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
