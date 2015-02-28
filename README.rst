m2bk
====

.. image:: https://travis-ci.org/axltxl/m2bk.svg?branch=develop

Send your mongodump backups straight to AWS S3
----------------------------------------------

*m2bk* is command line tool that performs a number of
**mongodb database backups via mongodump**, compresses them into a
gzipped tarball and finally sends them to an **AWS S3 bucket**.

.. image:: http://i.imgur.com/7uiVOSI.gif

-  `Requirements <#requirements>`_
-  `Contributing <#contributing>`_
-  `Installation <#installation>`_
-  `Basic usage <#basic-usage>`_
-  `Options <#options>`_
-  `Configuration file <#configuration-file>`_

   -  `Sections and directives <#configuration-file-sections-and-directives>`_

      -  `fs section <#fs-section>`_
      -  `mongodb section <#mongodb-section>`_

         -  `mongodb.host_defaults section <#mongodbhost_defaults-section>`_
         -  `mongodb.hosts section <#mongodbhosts-section>`_

      -  `aws section <#aws-section>`_
-  `Copyright and licensing <#copyright-and-licensing>`_

Requirements
============

-  `python <http://python.org>`_ >= 3.3
-  `boto <http://docs.pythonboto.org/en/latest/>`_ >= 2.33
-  `envoy <https://pypi.python.org/pypi/envoy>`_ >= 0.0.3
-  `pyyaml <http://pyyaml.org>`_ >= 3.11
-  `mongodb <http://www.mongodb.org>`_ >= 2.4


Contributing
============

There are many ways in which you can contribute to m2bk.
Code patches are just one thing amongst others that you can submit to help the project.
We also welcome feedback, bug reports, feature requests, documentation improvements,
advertisement and testing.

Feedback contributions
----------------------

This is by far the easiest way to contribute something.
If you’re using m2bk for your own benefit, don’t hesitate sharing.
Feel free to `submit issues and enhancement requests. <https://github.com/axltxl/m2bk/issues>`_

Code contributions
------------------

Code contributions (patches, new features) are the most obvious way to help with the project’s development.
Since this is so common we ask you to follow our workflow to most efficiently work with us.
For code contributions, we follow the "fork-and-pull" Git workflow.


1. Fork, then clone your repo on GitHub
::

  git clone git@github.com:your-username/m2bk.git
  git add origin upstream https://github.com/axltxl/m2bk.git

If you already forked the repo, then be sure to merge
the most recent changes from "upstream" before making a pull request.
::

  git pull upstream

2. Create a new feature branch in your local repo
::

  git checkout -b my_feature_branch

3. Make your changes, then make sure the tests passes
::

  virtualenv pyve && source pyve/bin/activate
  python3 setup.py test

4. Commit your changes once done
::

  git commit -a -m "My commit message"
  git push origin my_feature_branch

5. Submit a `pull request <https://github.com/axltxl/m2bk/compare/>`_ with your feature branch containing your changes.

Installation
============

Installation of m2bk can be made directly from source, via `pip <https://github.com/pypa/pip>`_ or
`easy_install <http://pythonhosted.org/setuptools/easy_install.html>`_, whichever you prefer.

Option # 1: pip
---------------
::

    $ pip install m2bk

Option # 2: from source
-----------------------
::

    $ git clone git@github.com:axltxl/m2bk.git
    $ cd m2bk
    $ python3 setup.py install

Option # 3: easy_install
------------------------
::

    $ easy_install m2bk

From this point you can edit your `configuration file <#configuration-file>`_
::

  $ vi /etc/m2bk/m2bk.yaml

Basic Usage
===========
Normal execution
::

  $ m2bk

Display output on stdout
::

  $ m2bk -s

Dry run
::

  $ m2bk -d

Specify an alternate configuration file
::

  $ m2bk -c /path/to/my/custom/m2bk.yaml


Options
=======
::

    m2bk [options]


-  ``--version`` show version number and exit
-  ``-h | --help`` show a help message and exit
-  ``-c [file] | --config=[file] | --config [file]`` specify configuration file to use
-  ``-d | --dry-run`` don't actually do anything
-  ``-s | --stdout`` log messages to stdout too
-  ``--ll | --log-level=[num]`` set logging output level

Configuration file
------------------

The configuration is handled through a simple `YAML <http://yaml.org/>`_
file including a series of *sections* (which are YAML objects), each one
composed by *directives* (YAML numbers, strings or arrays), these will
determine a corresponding behavior on **m2bk**. If **m2bk** does not receive
any configuration file on command line, it will try to read ``/etc/m2bk.yaml``.
**Please note the configuration format is still a work in progress and will most likely change in the early stages of m2bk.**


The following is an example of what a configuration file looks like:

::

  ---
  aws:
    aws_id: "SDF73HSDF3663KSKDJ"
    aws_access_key: "d577273ff885c3f84dadb8578bb41399"
  fs:
    output_dir: "/opt/tmp/mydir"
  mongodb:
    mongodump: "/opt/bin/mongodump"
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
        auth_db: bar
        dbs:
            - customers
            - sessions

Through this configuration file, you can set key variables about the
databases you want to backup and the AWS S3 bucket you wish to send them
to.

Configuration file: sections and directives
-------------------------------------------

``fs`` section
^^^^^^^^^^^^^^

This section has directives regarding files and directories manipulation

Directives
^^^^^^^^^^

``fs.output_dir``
"""""""""""""""""

-  Type: **string**
-  Default value : ``/tmp/m2bk``
-  Role: directory where m2bk is going to temporarily save backup files


``mongodb`` section
^^^^^^^^^^^^^^^^^^^

This section holds directives regarding mongodb servers **m2bk** is going
to connect to, including databases that are going to be backed up through *mongodump*.

**Example**:
::

    mongodb:
        mongodump: "/opt/bin/mongodump"
        host_defaults:
            user_name: tom
            address: db.example.local
            password: "457893mnfs3j"
            dbs:
              - halloran
              - grady
        hosts:
            foo:
                address: db0.example.internal
                port: 27654
                user_name: matt
                password: "myS3cr37P455w0rd"
                dbs:
                  # This list is going to be merged with dbs at host_defaults, thus
                  # the resulting dbs will be: 
                  # ['halloran', 'grady', 'jack', 'wendy', 'danny']
                  - jack
                  - wendy
                  - danny
            bar: {} # This one is going to acquire all host_defaults values
            host_with_mixed_values:
                # This host will inherit port, password and dbs from host_defaults
                address: moloko.example.internal
                user_name: alex
                address: localhost
                auth_db: milk_plus


Directives
^^^^^^^^^^

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
directives are ``user_name``, ``password``, ``port``, ``dbs`` and ``auth_db`` .
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
"""""""""""""""""""""""""""

-  Type: **string**
-  Required: YES
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

``mongodb.hosts.*.auth_db``
"""""""""""""""""""""""""""

-  Type: **string**
-  Required: NO
-  Default value : ``admin``
-  Role: authentication database

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


Copyright and Licensing
=======================

Copyright (c) Alejandro Ricoveri

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