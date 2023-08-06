===================
Simple Email-Sender
===================

This package provides a simple notifier sending emails.

* Free software: GNU General Public License v3
* Copyright (c) 2021 Henning Janssen

Installation
------------

To install the package, simply run within your terminal:

.. code-block:: sh

    $ pip install simple_email_sender

Usage
-----

You will need only one single line, to trigger a message within your Python code:

.. code-block:: python

    sender.info("Hello World")

For a fully working example, you need to specify the `server_settings` in a separate file

.. code-block:: yaml

    # server_settings.yaml

    # Use this file to store the server setting for the SMTP-Server

    "name": "example@email.com"
    "password": "MySecretPassword"
    "server": "smtp.example.com"
    "port": 465

And this is a MWE:

.. code-block:: python

    # example.py

    from simple_email_sender import Sender

    # Before running this example, you need to change your settings in the
    # 'server_settings.yaml'-file according to your personal needs


    def main():
        receiver = "example@email.com"
        sender = Sender("./server_settings.yaml", receiver, subject="Experiment 123")
        sender.info("Hello World")
        sender.error("Something unexpected happened and you should take care of it...")


    if __name__ == "__main__":
        main()
