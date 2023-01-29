
## Cryptedit


**Cryptedit** is a simple text editor that allows you to edit, encrypt and decrypt text files.
 

**Author:**
<i>Copyright (c) 2022-2023 Tiago C. Teixeira</i>

This is a python3 gui app that uses Gtk, so it depends on [Python bindings for GObject Introspection pachage](https://pypi.org/project/PyGObject/).
It also depends on python cryptographic library [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)

This packages can be installed with pip:

To install *Gtk* bindinds:<br/>
<b>$ pip install PyGObject</b>

To install *pycryptodome* library:<br/>
<b>$ pip install pycryptodome</b>

To install pip for Python 3 on Ubuntu 20.04 or later run the following commands as root or sudo user in your terminal:

<b>$ sudo apt update</br>
$ sudo apt install python3-pip</b>

To run the app from your terminal type:</br>
<b>$ python3 cryptedit.py</b>

### The encryption process
To encrypt the text you only need to provide a plain text password, which will also be required for decryption.
For the encryption process, the AES algorithm will be used with a 256-bit key. This key is derived from the password and a randomly generated set of bytes (salt), using the standard PBKDF2 derivation algorithm. An initialization vector (IV) consisting of 16 bytes also randomly generated is used.
For each new encryption process, a new salt and a random IV will be generated. These bytes are not secret and are saved together with the encrypted content, as they will be needed later to decrypt the content. The only secret is the password (key) that you will have to provide to decrypt it.


## Further references

 * https://pycryptodome.readthedocs.io/en/latest/src/introduction.html
 * https://pypi.org/project/PyGObject/
 * https://pypi.org/project/pip/
 * https://python-gtk-3-tutorial.readthedocs.io/en/latest/


