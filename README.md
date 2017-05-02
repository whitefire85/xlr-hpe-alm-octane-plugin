# xlr-hpe-alm-octane-plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-hpe-alm-octane-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-hpe-alm-octane-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/41acaeab16624f9fa221304eaaf62d20)](https://www.codacy.com/app/erasmussen39/xlr-hpe-alm-octane-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-hpe-alm-octane-plugin&amp;utm_campaign=Badge_Grade)
[![Code Climate](https://codeclimate.com/github/xebialabs-community/xlr-hpe-alm-octane-plugin/badges/gpa.svg)](https://codeclimate.com/github/xebialabs-community/xlr-hpe-alm-octane-plugin)
[![License: MIT][xlr-bitbucket-plugin-license-image] ][xlr-bitbucket-plugin-license-url]
[![Github All Releases][xlr-bitbucket-plugin-downloads-image]]()

[xlr-bitbucket-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-bitbucket-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-bitbucket-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-hpe-alm-octane-plugin/total.svg

## Preface
This document describes the functionality provided by the `xlr-hpe-alm-octane-plugin`

## Overview
This module offers a basic interface to HPE ALM Octane functionality.

## Installation
Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.

## Octane Authentication CI
Defines the information about the Octane server you wish to connect to. You must have the Client ID and Client Secret from the server to access the REST API.

![OctaneSharedConfigurationItem](images/octane_shared_config.png)

## Octane Tasks

### Get Epics
The Get Epics task will retrieve a list of Epic objects from the specified shared space and workspace.

![OctaneGetEpics](images/octane_get_epics.png)

---

## References:
