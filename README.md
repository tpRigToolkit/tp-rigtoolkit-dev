tpRigToolkit-dev
============================================================

Development repository for tpRigToolkit

.. image:: https://img.shields.io/badge/Python-2.7-yellow?logo=python
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/Python-3.7-yellow?logo=python
    :target: https://www.python.org/

.. image:: https://img.shields.io/badge/Windows-blue?logo=windows
    :target: https://www.python.org/

Requirements
============================================================

* **Python 2.7** or **Python 3.7** installed in your machine.

    .. note::
        Scripts expect to find Python executables in their default locations:
            * **Python 2**: C:\Python27
            * **Python 3**: C:\Python37

        You can edit **setup_venv_py2.bat** and **setup_venv_py3.bat** if you want to use custom Python installation directories

* Make sure **virtualenv** is installed:

      .. code-block::

            pip install virtualenv


* Make **Git** client is installed : https://git-scm.com/


How to use
============================================================

1. Run **setup_repos.bat** to automatically download from GitHub all tpDcc & tpRigToolkit related repositories.

2. Run:
    - **setup_venv_py2.bat**: to create virtual environment for Python 2.
    - **setup_venv_py3.bat**: to create virtual environment for Python 3.

3. Run **setup_vendors.bat** to install all specific DCC related repositories.

4. Execute **tprigtoolkit_main.py** in your favorite Python DCC editor to load tpDcc :)