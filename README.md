# release-process-automation

Automating the Release process using [Bitergia/release-tools](https://github.com/Bitergia/release-tools), [Poetry](https://python-poetry.org), and [GitHub Actions](https://docs.github.com/en/actions).

This work was designed and implemented for the GrimoireLab toolset. As of now, the whole workflow is supported only for Python projects. But, this can be tailored and used for any project.

This work is licensed under GPL3 or later.

## Features

This combination of the tools allows us to:
- manage your releases of your python project with proper versioning and release notes
- build the packages and test them against the test suite
- publish packages to PyPI

## Requirements

- Poetry should be configured to your Python project. The `pyproject.toml` file must also be tracked on your repository. See [The pyproject.toml file | Documentation | Poetry](https://python-poetry.org/docs/pyproject) for more information.
- The project should have a `_version.py` file. This file must also be tracked on your repository. It must contain a variable named `__version__`. The value must be a string following semantic versioning format.
```
$ cat _version.py
__version__ = "3.6.5"
```
- The project should have `NEWS` and `AUTHORS` files.
- Projected should be hosted on GitHub as we use GitHub Actions.

## Workflow

1. Once you have all the required files, you can start using the [Bitergia/release-tools](https://github.com/Bitergia/release-tools). The **workflow** is defined by the next steps:
    ```
        changelog -> semverup -> notes -> publish
    ```
2. Developers use [changelog](https://github.com/Bitergia/release-tools#changelog) script to generate changelog **entry notes**. They contain basic information about their changes in the code (e.g a new feature; a fixed bug). The notes should **explain** the change to a reader who has **zero context** about software details.\
We **recommend** to create one of these entries for each pull request or merge request.\
These notes are stored under the directory `releases/unreleased`.
    ```
    $ changelog -t "Add sum method" -c added
    Changelog entry 'add-sum-method.yml' created
    ```
    Example: [releases/unreleased/add-sum-method.yml](https://github.com/vchrombie/release-process-automation/blob/0a41b9fbcc763d67d845b4abc81b1d251c6207f5/releases/unreleased/add-sum-method.yml)
3. Once we are ready to create a new release, we call [semverup](https://github.com/Bitergia/release-tools#semverup). It will increase the **version** according to [semantic versioning](https://semver.org) and the type of changelog entries generated between releases.
    ```
    $ semverup
    0.1.0
    ```
4. When the version is increased, we run [notes](https://github.com/Bitergia/release-tools#notes) to generate the **release notes** using the unreleased changelog entries. You can update the `AUTHORS` & `NEWS` files, using the `--authors` & `--news` flags respectively.
    ```
    $ notes "calculator" 0.1.0
    Release notes file '0.1.0.md' created
    ```
    Example: [releases/0.1.0.md](https://github.com/vchrombie/release-process-automation/blob/master/releases/0.1.0.md)
5. Finally, we **publish** the release in the Git repository creating a **commit** that will contain the new release notes and the new version files. A **tag** is also created with the new version number. To do it, we call to [publish](https://github.com/Bitergia/release-tools#publish) script. This script also removes the entries in `released/unreleased` directory.
    ```
    $ publish 0.1.0 "Venu Vardhan Reddy Tekula <venuvardhanreddytekula8@gmail.com>" --push origin
    Cleaning directories...done
    Adding files to the release commit...done
    Creating release commit...done
    Publishing release in origin...done
    ```
    Example:
    - [vchrombie/release-process-automation/commit/d87dadf260601b658987cb5787ba0918c71e05d1](https://github.com/vchrombie/release-process-automation/commit/d87dadf260601b658987cb5787ba0918c71e05d1)
    - [vchrombie/release-process-automation/tree/0.1.0](https://github.com/vchrombie/release-process-automation/tree/0.1.0)
6. Once the release and the tag is pushed to GitHub, GitHub Actions will be triggered and the release workflow will be initiated.
    ```
    name: release
    on:
      push:
        tags:
          - '*.*.*'
          - '*.*.*-*'
    ```
    Release Workflow File: [.github/workflows/release.yml](https://github.com/vchrombie/release-process-automation/blob/master/.github/workflows/release.yml)
7. The release workflow has 4 steps (or jobs).
    ```
        build -> tests -> release -> publish
    ```
8. Poetry can be used to generate the wheel archives using `poetry build`. Later, the distributions is uploaded to re-use in the next steps.
    ```
    - name: Build distributions
      run: |
        poetry build
    - name: Upload distribution artifacts
      uses: actions/upload-artifact@v2
      with:
        name: calculator-dist
        path: dist
    ```
9. Now, we have the wheel packages ready. We would like to test the package by running the test suite. The dev-dependencies are not available in the package, so we can install it using [vchrombie/peodd](https://github.com/vchrombie/peodd).
    ```
    - name: Download distribution artifact
      uses: actions/download-artifact@v2
      with:
        name: calculator-dist
        path: dist
    - name: Install dev dependencies
      run: |
        pip install peodd
        peodd -o requirements-dev.txt
        pip install -r requirements-dev.txt
    - name: Test package
      run: |
        PACKAGE_NAME=`(cd dist && ls *whl | cut -f 1 -d "-")` && echo $PACKAGE_NAME
        pip install --pre --find-links ./dist/ $PACKAGE_NAME
        pytest
    ```
10. The release will published on the GitHub and the release notes generated using the `notes` script will be used.
    ```
    - name: Get release tag
      id: tag
      run: |
        echo ::set-output name=tag::${GITHUB_REF#refs/tags/}
    - name: Create release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ steps.tag.outputs.tag }}
        release_name: ${{ steps.tag.outputs.tag }}
        body_path: ./releases/${{ steps.tag.outputs.tag }}.md
    ```
11. Finally, the wheel distributions are uploaded to PyPI using Poetry. Make sure you store the `PYPI_API_TOKEN` which is needed for the authentication to upload the package.
    ```
    - name: Download distribution artifact
      uses: actions/download-artifact@v2
      with:
        name: calculator-dist
        path: dist
    - name: Configure pypi credentials
      env:
        PYPI_API_TOKEN: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        poetry config http-basic.pypi __token__ "$PYPI_API_TOKEN"
    - name: Publish release to pypi
      run: |
        poetry publish
    ```
12. The work is currently being implemented in the GrimoireLab Repositories, after some successful trials.
    - https://github.com/chaoss/grimoirelab-toolkit/blob/master/.github/workflows/release.yml
    - https://github.com/chaoss/grimoirelab-toolkit/releases/tag/0.2.0
    - https://pypi.org/project/grimoirelab-toolkit/0.2.0

## Acknowledgment

- Big credit to [@sduenas](https://github.com/sduenas/) for the idea, work around [Bitergia/release-tools](https://github.com/Bitergia/release-tools) and constantly helping, suggesting ideas & reviewing the work.

## License

Licensed under GNU General Public License (GPL), version 3 or later.
