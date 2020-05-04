.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/dvrhax/uPyMySQL/blob/master/LICENSE


uPyMySQL
=======

.. contents:: Table of Contents
   :local:

This package contains a pretty rough hack of the pure-Python MySQL client library. The goal of uPyMySQL
is to be a drop-in replacement for MySQLdb and work on uPython.

NOTE: PyMySQL doesn't support low level APIs `_mysql` provides like `data_seek`,
`store_result`, and `use_result`. You should use high level APIs defined in `PEP 249`_.
But some APIs like `autocommit` and `ping` are supported because `PEP 249`_ doesn't cover
their usecase.  Ditto for uPyMySQL

.. _`PEP 249`: https://www.python.org/dev/peps/pep-0249/

Requirements
-------------

* uPython_

* MySQL Server -- one of the following:

  - MySQL_ >= 4.1  (tested with only 5.5~)
  - MariaDB_ >= 5.1

.. _uPython: https://micropython.org/
.. _MySQL: http://www.mysql.com/
.. _MariaDB: https://mariadb.org/


Installation
------------

    Clone from Git and copy the upymysql folder onto your microcontroller
    Most likely directly copying onto your microcontroller will fail.  
    You will likely need to re-compile micropython including upymysql into the firmware


Documentation
-------------

    You're pretty much looking at it

Example
-------

No Guarantees that these work yet:

The following examples make use of a simple table

.. code:: sql

   CREATE TABLE `users` (
       `id` int(11) NOT NULL AUTO_INCREMENT,
       `email` varchar(255) COLLATE utf8_bin NOT NULL,
       `password` varchar(255) COLLATE utf8_bin NOT NULL,
       PRIMARY KEY (`id`)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
   AUTO_INCREMENT=1 ;


.. code:: python

    import upymysql
    import upymysql.cursors

    # Connect to the database
    connection = upymysql.connect(host='localhost',
                                 user='user',
                                 password='passwd',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=upymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

This example will print:

.. code:: python

    {'password': 'very-secret', 'id': 1}


Resources
---------

DB-API 2.0: http://www.python.org/dev/peps/pep-0249

MySQL Reference Manuals: http://dev.mysql.com/doc/

MySQL client/server protocol:
http://dev.mysql.com/doc/internals/en/client-server-protocol.html

PyMySQL mailing list: https://groups.google.com/forum/#!forum/pymysql-users

PyMySQL Github site: https://github.com/PyMySQL/PyMySQL

uPython: https://micropython.org/

License
-------

PyMySQL is released under the MIT License. See LICENSE for more information.
