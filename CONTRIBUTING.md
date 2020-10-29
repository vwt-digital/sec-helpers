# Contributing to Sec-helpers
Thank you for contributing to Sec-helpers! These guidelines might help us understand new issues and enhancements better!

## VWT Digital Guidelines
Read these guidelines before creating issues or requests.
[vwtdigital.CONTRIBUTING](https://github.com/vwt-digital/operational-data-hub/blob/develop/vwtdigital.CONTRIBUTING.md)

## What should I know before I get started?
Sec-helpers is actively being used by [Cloudbuilder-DAST](https://github.com/vwt-digital/cloudbuilder-dast) to test every deployed project.<br>

**Important to know**: NoSsl requires requires
[openssl-1.0.2](https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz).
If NoSsl does not want to run, because the required version does not match the local version,
try to run [Cloudbuilder-DAST](https://github.com/vwt-digital/cloudbuilder-dast) in a container.
You can build a version of Python with the right version of openssl, like we do [here](https://github.com/vwt-digital/cloudbuilder-dast/blob/develop/Dockerfile#L10),
but we can't recommend you do this. <br>
Please **do not** create a pull request to update this package to a newer version without verifying that the functionality stays the same. A suggestion in an enhancement issue is fine.

## VWT Digital
- :mailbox: [Contact us](https://vwt-digital.github.io/#contact)
- :house: [About us](https://vwt-digital.github.io/)
- :zap: [Github](https://github.com/vwt-digital)
