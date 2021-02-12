*********************************
Continuous Integration (CircleCI)
*********************************

.. admonition:: What is continuous integration?

   Continuous integration (CI) is a software development strategy that increases the speed of development while ensuring
   the quality of the code that teams deploy. Developers continually commit code in small increments (at least daily, or
   even several times a day), which is then automatically built and tested before it is merged with the shared repository.

   Source: `CircleCI documentation <https://circleci.com/continuous-integration/>`__


Configuration
=============

Our CircleCI configuration resides in :github-source:`.circleci/config.yml`.
It contains all the jobs listed below.
See `Configuring CircleCI <https://circleci.com/docs/2.0/configuration-reference/>`__ for a full reference.


Workflow ``main``
=================

.. image:: images/circleci-main-workflow.png
    :alt: CircleCI main workflow

pipenv-install
--------------

This job executes ``pipenv install --dev`` and makes use of the `CircleCI Dependency Cache <https://circleci.com/docs/2.0/caching/>`__.
It passes the virtual environment ``.venv`` to the subsequent jobs.

npm-install
-----------

This job executes ``npm install`` and makes use of the `CircleCI Dependency Cache <https://circleci.com/docs/2.0/caching/>`__.
It passes the installed ``node_modules`` to the subsequent jobs.

pylint
------

This job executes ``pipenv run pylint_runner``, which checks whether the :ref:`pylint` throws any errors or warnings.

black
-----

This job executes ``pipenv run black --check .``, which checks whether the code matches the :ref:`black-code-style` code style.

tests
-----

This job runs the unit tests. It sets up a temporary postgres database and runs the migrations before testing.
It uses the command ``pipenv run integreat-cms-cli test cms --set=COVERAGE --settings=backend.circleci_settings`` and
passes the coverage in the ``htmlcov`` directory to the build artifacts.

check-translations
------------------

This job uses the dev-tool ``./dev-tools/check_translations.sh`` to check whether the translation file is up to date and
does not contain any empty or fuzzy entries.

.. _circleci-bundle-static-files:

bundle-static-files
-------------------

This job compiles and compresses all static files, e.g. CSS, JS as well as the compiled translation file.
It passes the resulting objects to the testing and packaging jobs.

.. _circleci-packaging:

packaging
---------

This job creates a debian package with ``python3 setup.py --command-packages=stdeb.command bdist_deb`` and passes the
resulting files in ``dist`` to the build artifacts.

build-documentation
-------------------

This job checks whether the documentation can be generated without any errors by running
``pipenv run ./dev-tools/generate_documentation.sh``.
It passes the html documentation in ``docs`` to the :ref:`circleci-deploy-documentation` job.

.. _circleci-deploy-documentation:

deploy-documentation
--------------------

This job authenticates as the user `IntegreatAPI <https://github.com/IntegreatAPI>`_ and commits all changes to the
documentation to the branch `gh-pages <https://github.com/Integreat/cms-django/tree/gh-pages>`_
which is then deployed to ``https://integreat.github.io/cms-django/`` by GitHub.

.. _circleci-docker-images:

docker-images
-------------
This job builds the docker images used for this CircleCI workflow (see :ref:`circleci-custom-docker-images` for more information).
After a successful docker build, the images are pushed to `Docker Hub <https://hub.docker.com/u/integreat>`__

To login to our organization's docker hub account, the job needs to access the secret ``DOCKER_PASSWORD``, which is
available to all users of the GitHub team `Integreat/cms <https://github.com/orgs/Integreat/teams/cms>`__.
This is also the reason why the job is not executed on branches of the dependabot, because the bot does not have the
permissions to access the Docker Hub credentials.

.. admonition:: Got error "Unauthorized"?
    :class: error

    If you get an ``Unauthorized`` error on this job, see :ref:`circleci-unauthorized`.


Debugging with SSH
==================

If you encounter any build failures which you cannot reproduce on your local machine, you can SSH into the build
server and examine the problem. See `Debugging with SSH <https://circleci.com/docs/2.0/ssh-access-jobs/>`__ for
more information.


.. _circleci-custom-docker-images:

Custom Docker Images
====================

To speed up the jobs :ref:`circleci-bundle-static-files` and :ref:`circleci-packaging`, we use the custom docker images
`integreat/python-node-gettext <https://hub.docker.com/r/integreat/python-node-gettext>`__ and
`integreat/bionic-setuptools <https://hub.docker.com/r/integreat/bionic-setuptools>`__.

.. Note::

    See `Using Custom-Built Docker Images <https://circleci.com/docs/2.0/custom-images/>`__ for more information on custom
    docker images for CircleCI builds.

The Dockerfiles are managed via GitHub in :github-source:`.circleci/images/bionic-setuptools/Dockerfile` and
:github-source:`.circleci/images/python-node-gettext/Dockerfile`.
Every time a change is pushed to GitHub (no matter on which branch), they are tagged with the commit's SHA1 hash and
pushed to `Docker Hub <https://hub.docker.com/u/integreat>`__ (see :ref:`circleci-docker-images` for more information).
Don't forget to change the image tag in :github-source:`.circleci/config.yml` after you made changes to the Dockerfile::

  bundle-static-files:
    docker:
      - image: integreat/python-node-gettext:<INSERT-NEW-COMMIT-SHA1-HERE>

  packaging:
    docker:
      - image: integreat/bionic-setuptools:<INSERT-NEW-COMMIT-SHA1-HERE>
