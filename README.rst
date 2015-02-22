m2bk
====

.. image:: https://travis-ci.org/axltxl/m2bk.svg?branch=develop

mongodump straight to Amazon S3
-------------------------------

*m2bk* is a small DevOps command line tool who performs a number of
**mongodb database backups via mongodump**, compresses them into a
gzipped tarball and finally sends them to an **AWS S3 bucket**.

-  `Requirements <#requirements>`_
-  `Issues <#issues>`_
-  `Contributing <#contributing>`_
-  `Copyright and licensing <#copyright-and-licensing>`_
-  `Usage <#usage>`_

   -  `Options <#options>`_

-  `Configuration file <#configuration-file>`_

   -  `Sections and directives <#configuration-file-sections-and-directives>`_

      -  `log section <#log-section>`_
      -  `mongodb section <#mongodb-section>`_

         -  `mongodb.host_defaults section <#mongodbhost_defaults-section>`_
         -  `mongodb.hosts section <#mongodbhosts-section>`_

      -  `aws section <#aws-section>`_

Requirements
============

-  `python <http://python.org>`_ >= 3.3
-  `boto <http://docs.pythonboto.org/en/latest/>`_ >= 2.33
-  `envoy <https://pypi.python.org/pypi/envoy>`_ >= 0.0.3
-  `pyyaml <http://pyyaml.org>`_ >= 3.11
-  mongodump >= 2.4

Issues
======

Feel free to submit issues and enhancement requests.

Contributing
============

Please refer to each project's style guidelines and guidelines for
submitting patches and additions. In general, we follow the
"fork-and-pull" Git workflow.

1. Fork the repo on GitHub
2. Commit changes to a branch in your fork
3. Pull request "upstream" with your changes
4. Merge changes in to "upstream" repo

NOTE: Be sure to merge the latest from "upstream" before making a pull
request!

Copyright and Licensing
=======================

Copyright (c) 2014 Alejandro Ricoveri

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Usage
=====

::

    m2bk [options]

Options
-------

-  ``--version`` show version number and exit
-  ``-h | --help`` show a help message and exit
-  ``-c [file] | --config=[file] | --config [file]`` specify configuration file to use
-  ``-d | --dry-run`` don't actually do anything
-  ``-s | --stdout`` log messages to stdout too
-  ``--ll | --log-level=[num]`` set logging output level

Installation
============

Once the source distribution has been downloaded, installation can be
made via **setuptools** or **pip**, whichever you prefer.

::

 $ # setuptools installation
 $ cd m2bk
 $ python setup.py install
 $ # from this point, you can create your configuration file
 $ vi /etc/m2bk/m2bk.yaml $ # Once installed, you can try it
 $ m2bk -c /path/to/myconfig.yaml``

If everything went well, you can then check out your S3 bucket to see
the backup.

Configuration file
------------------

The configuration is handled through a simple `YAML <http://yaml.org/>`_
file including a series of *sections* (which are YAML objects), each one
composed by *directives* (YAML numbers, strings or arrays), these will
determine a corresponding behavior on **m2bk**.

If **m2bk** does not receive any configuration file on command line,
it will try to read ``/etc/m2bk.yaml``.

The following is an example of what a configuration file looks like:

::

  ---
  debug: true
  aws:
    aws_id: "SDF73HSDF3663KSKDJ"
    aws_access_key: "d577273ff885c3f84dadb8578bb41399"
    mongodb:
      mongodump: "/opt/bin/mongodump"
      output_dir: "/opt/tmp/mydir"
      host_defaults:
        port: 666
        user_name: "satan"
        password: "14mh4x0r"
        hosts:
          foo:
            address: "foo.example.local"
            port: 34127
            dbs:
              - "app"
              - "sessions"
              - "another_one"
            bar:
              address: "bar.example.com"
              password: "1AmAn07h3rh4x0r"

Through this configuration file, you can set key variables about the
databases you want to backup and the AWS S3 bucket you wish to send them
to.

Configuration file: sections and directives
-------------------------------------------

Root section directives
^^^^^^^^^^^^^^^^^^^^^^^

``debug``
"""""""""

- Type: **boolean**
- Default value: ``false``
- Role: Debug mode is activated if ``true``

``mongodb`` section
^^^^^^^^^^^^^^^^^^^

This section holds directives regarding `mongodb <http://mongodb.org>`_ servers **m2bk** is going
to connect to, including databases that are going to be backed up through *mongodump*.

**Example**:
::

    mongodb:
        mongodump: "/opt/bin/mongodump"
        output_dir: "/tmp/backups"
        host_defaults:
            user_name: tom
            address: db.example.local
            password: "457893mnfs3j"
            dbs:
              - "test"
              - "test2"
        hosts:
            foo:
                address: db0.example.internal
                port: 27654
                user_name: matt
                password: "myS3cr37P455w0rd"
                dbs:
                  - "jack"
                  - "wendy"
                  - "danny"
            bar: {} # This one is going to acquire all host_defaults values
            host_with_mixed_values:
                # This host will inherit port, password and dbs from host_defaults
                user_name: jeff
                address: localhost


Directives
^^^^^^^^^^

``mongodb.output_dir``
""""""""""""""""""""""

-  Type: **string**
-  Default value : ``/tmp/m2bk``
-  Role: directory where m2bk is going to temporarily save backup files

``mongodb.mongodump``
"""""""""""""""""""""

-  Type: **string**
-  Default value : ``mongodump``
-  Role: full path to the ``mongodump`` executable used by m2bk

``mongodb.host_defaults`` section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many directives (such as user name and/or password) could be common
among the databases that are going to be backed up. For this reason, it
is best to simply put those common directives under a single section,
this is entirely optional but also it is the best for easily manageable
configuration files in order to avoid redundancy, the supported
directives are ``user_name``, ``password``, ``dbs`` and ``port`` .
See ``hosts`` section.

``mongodb.hosts`` section
^^^^^^^^^^^^^^^^^^^^^^^^^

This is an object/hash, where each element contains a series of
directives relative to a mongodb database located at a server, its
specifications and databases themselves held by it, these are
the main values used by ``mongodump`` when it does its magic. For each
entry inside the ``hosts`` section, these are its valid directives:


Directives
^^^^^^^^^^

``mongodb.hosts.*.address``
""""""""""""""""""""""""""""

-  Type: **string**
-  Required: YES
-  Default value : "localhost"
-  Role: mongodb server location

``mongodb.hosts.*.port``
""""""""""""""""""""""""

-  Type: **integer**
-  Required: NO
-  Default value : ``mongo.host_defaults.port | 27017``
-  Role: mongodb server listening port

``mongodb.hosts.*.user_name``
"""""""""""""""""""""""""""""

-  Type: **string**
-  Required: NO
-  Default value : ``mongodb.host_defaults.user_name | m2bk``
-  Role: user name used for authentication against the mongodb server

``mongodb.hosts.*.password``
""""""""""""""""""""""""""""

-  Type: **string**
-  Required: NO
-  Default value : ``mongodb.host_defaults.pass | "pass"``
-  Role: password used for authentication against the mongodb server

``mongodb.hosts.*.dbs``
"""""""""""""""""""""""

-  Type: **array**
-  Required: NO
-  Default value : ``mongodb.host_defaults.dbs | []``
-  Role: a list of databases who are expected inside the mongodb server

**NOTE: particular "dbs" on one host will be merged with those of "host_defaults"**

``aws`` section
^^^^^^^^^^^^^^^

This sections holds directives regarding AWS credentials that **m2bk**
is going to use in order to upload the *mongodump* backups to S3.

**Example**:
::

    aws:
        aws_id": "HAS6NBASD8787SD"
        aws_access_key: "d41d8cd98f00b204e9800998ecf8427e"
        s3_bucket: "mybucket"

Directives
^^^^^^^^^^

aws.aws_id
""""""""""

-  Type: **string**
-  Required: NO
-  Default value : ``""``
-  Role: AWS access key ID


``aws.aws_access_key``
""""""""""""""""""""""

-  Type: **string**
-  Required: NO
-  Default value : ``""``
-  Role: AWS access key ID

``aws.s3_bucket``
"""""""""""""""""

-  Type: **string**
-  Required: NO
-  Default value: ``m2bk``
-  Role: name of the main S3 bucket where m2bk is going to upload the compressed backups for each mongodb server specified in ``mongodb`` section
