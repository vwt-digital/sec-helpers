# Contributing to Sec-helpers
Thank you for contributing to Sec-helpers. The following guidelines can help us understand the new addition or issue.

## Quick Access
[Reporting Issues](#reporting-issues)

[Suggesting enhancements](#suggesting-enhancements)

[Pull Requests](#pull-requests)
* [Steps](#steps)
* [Message Guidelines](#message-guidelines)
* [Code Guidelines](#code-guidelines)
    * Architecture Decision Records
    * Code
    * Tests

[What should I know before I get started?](#what-should-i-know-before-i-get-started)

[VWT Digital](#vwt-digital)

## Reporting issues

It is incredibly helpful when issues or bugs are reported. To ensure that these issues can be solved as quickly and as goal oriented as possible, we've but together some guidelines for submitting issues.

- **Use a clear title** and be descriptive. This is important, because it allows us to evaluate importance between issues.
- Start the issue with **a description of where you found the issue**. This allows us to read the rest with a clear insight of what component we need to look at.
- **Describe how we can reproduce the issue.** Try to describe the exact steps you took.
- **Include the output** of any scripts that ran during or before the issue occured.
- **Describe what you expected to happen** and how that is different to what happened.
- If you created a solution, **please create a Pull Request** and link it.

Read [What should I know before I get started?](#what-should-i-know-before-i-get-started) before making changes.

## Suggesting enhancements

New ideas or enhancements are always helpful and welcome! To help us understand the idea better, we've put together some guidelines for submitting these suggestions.

- **Use a clear title** and be descriptive.
- Start the issue with **a description of what component will need to receive the enhancement**. This allows us to read the rest with a clear insight of what component we need to look at.
- **Describe what the enhancement is and what is should do**. Be as clear as possible, and try to add possible outputs to the description.
- **Describe why the enhancement should be added** to the project.
- Already changed some code? **Create a Pull Request** and link it to the suggestion!

Read [What should I know before I get started?](#what-should-i-know-before-i-get-started) before making changes.

## Pull Requests

New additions to the project are welcome! To help us understand the new addition better, we've put together some guidelines for submitting a pull request.

#### Steps
1. Follow the Message Guidelines.
2. Create a new pull request that describes what changed (Should follow Message Guidelines)
3. Describe what changed.
4. Describe why it was changed. Link issues if possible.
5. If possible, run [Cloudbuilder-SAST](https://github.com/vwt-digital/cloudbuilder-sast), and add the console output. This increases the chances of a positive merge and build.

Read [What should I know before I get started?](#what-should-i-know-before-i-get-started) before making changes.

#### Message Guidelines 
- Use past tense (Do: `Removed ...`, don't: `Remove ...`. Do: `Added ...`, don't: `Add ...`)
- Act as you take the action (Do: `Moved ...`, don't `Moves ...`)
- Messages should not contain emojis. (Do: `Deleted ...`, don't: :apple: ...)
- References to issues should be added, if possible (Do: `... #2`, don't: `... Trello-12`)
- We use Jira Tickets, you shouldn't (Do: `... #2`, don't: `... DAT-0000`)

#### Code Guidelines

**Architecture Decision Records**<br>
We use ADR's to ensure that decisions made by different developers will still result in the same guidelines being followed.
While the list greatly expands outside of the scope of this project, it might still be an interesting read:<br>
[Our Architecture Decision Records](https://github.com/vwt-digital/operational-data-hub/tree/develop/architecture/adr)

**Code**<br>
We follow best practices and coding styles that are described by the creator. For some languages, we increased the guidelines:
- Python
  - [pep8](https://pep8.org/)
  - [pylint](https://www.pylint.org/)
- Node.js
  - [Style guide](https://github.com/felixge/node-style-guide)

**Tests**<br>
Running the following test/checks/validators/linters will increase the integrity of the project.

[Cloudbuilder-SAST](https://github.com/vwt-digital/cloudbuilder-sast): <br>
*We run these tests on every project*
- [shellcheck](https://www.shellcheck.net/)
- [yamllint](http://www.yamllint.com/)
- custom json linter (any JSON linter/validator will do)
- [trufflehog](https://github.com/dxa4481/truffleHog)
- [bandit](https://pypi.org/project/bandit/) 
- [flake8](https://pypi.org/project/flake8/)
- [eslint](https://eslint.org/)

[Cloudbuilder-DAST](https://github.com/vwt-digital/cloudbuilder-dast): <br>
*We run these tests on projects that are deployed and accessible on the web*
- [Sec-helpers](https://pypi.org/project/sec-helpers/)

[Cloudbuilder-unittest](https://github.com/vwt-digital/cloudbuilder-unittest): <br>
*We run these tests on API projects that are deployed and accessible on the web*
- [Openapi3-fuzzer](https://pypi.org/project/openapi3-fuzzer/)

Extra: <br>
- [Zally](https://github.com/zalando/zally) for API specification files.
- [e2e-api-coverage](https://github.com/vwt-digital/e2e-api-coverage) after e2e tests.

## What should I know before I get started?
Sec-helpers is actively being used by [Cloudbuilder-DAST](https://github.com/vwt-digital/cloudbuilder-dast) to test every deployed project.<br>

**Important to know**: NoSsl requires requires
[openssl-1.0.2](https://www.openssl.org/source/old/1.0.2/openssl-1.0.2k.tar.gz).
If NoSsl does not want to run, because the required version does not match the local version,
try to run [Cloudbuilder-DAST](https://github.com/vwt-digital/cloudbuilder-dast) in a container.
You can build a version of Python with the right version of openssl, like we do [here](https://github.com/vwt-digital/cloudbuilder-dast/blob/develop/Dockerfile#L10),
but we can't recommend you do this. <br>
Please **DO NOT** create a pull request to update this package to a newer version. A suggestion in an enhancement issue is fine.

## VWT Digital
- :mailbox: [Contact us](https://vwt-digital.github.io/#contact)
- :house: [About us](https://vwt-digital.github.io/)
- :zap: [Github](https://github.com/vwt-digital)

