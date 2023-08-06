.. _IntegrationTests:

#########################
IntegrationTests
#########################

.. update the following links to point to your package
.. image:: https://img.shields.io/badge/SAL-API-gray.svg
    :target: https://ts-xml.lsst.io/sal_interfaces/IntegrationTests.html
.. image:: https://img.shields.io/badge/GitHub-gray.svg
    :target: https://github.com/lsst-ts/ts_IntegrationTests
.. image:: https://img.shields.io/badge/Jira-gray.svg
    :target: https://jira.lsstcorp.org/issues/?jql=labels+%3D+ts_IntegrationTests
.. image:: https://img.shields.io/badge/Jenkins-gray.svg
    :target: https://tssw-ci.lsst.org/job/LSST_Telescope-and-Site/job/ts_IntegrationTests/

.. Warning::

   **This integration testing documentation is under development and not ready for active use.**

.. _Overview:

Overview
========

[This section is to present an overview of the integration testing.
This should include a top-level description of the primary use-case(s) as well as any pertinent information.
Example information may be link(s) to the higher-level classes which may be used to operate it, or mention of other packages (with links) that it operates in concert with.]

.. note:: If you are interested in viewing other branches of this repository append a `/v` to the end of the url link. For example `https://ts_IntegrationTests.lsst.io/v/`


.. _User_Documentation:

User Documentation
==================

.. This template has the user documentation in a subfolder.
.. However, in cases where the user documentation is extremely short (<50 lines), one may move that content here and remove the subfolder.
.. This will require modification of the heading styles and possibly renaming of the labels.
.. If the content becomes too large, then it must be moved back to a subfolder and reformatted appropriately.

User-level documentation, found at the link below, is aimed at personnel looking to perform the standard use-cases/operations with the IntegrationTests.

.. toctree::
    user-guide/user-guide
    :maxdepth: 2

.. _Configuration:

Configuring the IntegrationTests
================================
.. For packages where configuration is not required, this section can contain a single sentence stating so.
   More introductory information can also be added here (e.g. package XYZ requires both a configuration file containing parameters as well as several look-up tables to be operational).

The configuration for the IntegrationTests is described at the following link.

.. toctree::
    configuration/configuration
    :maxdepth: 1


.. _Testing_Documentation:

Testing Documentation
=====================

.. This template has the user documentation in a subfolder.
.. However, in cases where the user documentation is extremely short (<50 lines), one may move that content here and remove the subfolder.
.. This will require modification of the heading styles and possibly renaming of the labels.
.. If the content becomes too large, then it must be moved back to a subfolder and reformatted appropriately.

This area of documentation focuses on the classes used, API's, and how to participate to the development of the IntegrationTests software packages.

.. toctree::
    tester-guide/tester-guide
    :maxdepth: 1

.. _VersionHistory:

Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each package will link to whatever method of tracking is being used for that package until standardization occurs.
.. No new work should be required in order to complete this section.

The version history of the IntegrationTests is found at the following link.

.. toctree::
    version-history
    :maxdepth: 1
