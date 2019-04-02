# Contributing to Zaaktypecatalogus

## Reporting issues

Please report issues to the upstream [gemma-zaken][gemma-zaken-issues]
repository.

We manage issues/bugs/userstories centralized so that they can be prioritized
by the product owner and planned into the sprint. There are templates available
for new user stories or bugs.

## Implementing features

We welcome enthusiasm for new features!

However, to prevent dissapointment, we recommend you to:

* create a user story in [gemma-zaken][gemma-zaken-issues] - it's possible that
  the conclusion is that we don't want to support that feature (for the time
  being)

* keep in mind that RGBZ 2, ImZTC 2.2 and RSGB 3 are the starting points.
  Deviations are possible if they fit into the bigger 'Common Ground' vision.

**Practical developer stuff**

The API specification is generated from the code, which is mostly driven by the
library [vng-api-common][vng-api-common]. Often, changes in there are needed
if features are bigger, and we recommend to install the dependency as an
editable dependency so you can create a PR for that as well:

```bash
pip install -e git+https://github.com/vng-Realisatie/vng-api-common#egg=vng-api-common
```

Once the code changes are done and verified to be functioning, you can update
the OAS 3.0 in the codebase by running:

```bash
generate_schema
```

**Style guides**

* we use `isort` to make sure imports are consistently sorted (config in `setup.cfg`)
* PEP8 applies to code formatting (config in `setup.cfg`)
* The [Django code-style][django-coding-style] applies as well
* the `.editorconfig` file contains configuration per file-type. Most editors
  should pick this up automatically.

## Suggesting API changes

We welcome you to suggest changes to the API itself! Please do so by making a
pull request in [gemma-zaken][gemma-zaken] (see the `api-specificatie`
directory in the root of the project).

Before the changes can be merged, we will need to update the reference
implementation(s) to reflect this.

[gemma-zaken]: https://github.com/vng-Realisatie/gemma-zaken
[gemma-zaken-issues]: https://github.com/vng-Realisatie/gemma-zaken/issues
[vng-api-common]: https://github.com/vng-Realisatie/vng-api-common
[django-coding-style]: https://docs.djangoproject.com/en/stable/internals/contributing/writing-code/coding-style/
