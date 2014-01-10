# How to contribute

Multiple controbutors are essential for ensuring the smooth running of
pyCourseSync. Batches will come and go, it is the current students that need to
adapt pyCourseSync to the requirements of the day. However, with multiple
controbutors, the source will soon get messy. We want to keep it as easy as
possible to contribute changes to pyCourseSync. There are a few guidelines that
we need contributors to follow so that the project remains maintainable.

## Getting Started

* Make sure you have a [GitHub account](https://github.com/signup/free)
* Create an issue in the parent repository for whatever problem you are facing.
  * Clearly describe the issue including steps to reproduce when it is a bug.
  * Make sure you fill in the earliest version that you know has the issue.
* Fork the repository on GitHub

## Making Changes

* Create a topic branch from where you want to base your work.
  * Usually, all new work should go be merged into Working.
  * To quickly create a topic branch based on Working; `git checkout -b
    your_branch_name Working`. Branch names should be logical and should
    describe the kind of changes being made in that branch. Please avoid
    working directly on the `master` and `Working` branches.
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.

```
    Fixes #2 Make the example in CONTRIBUTING imperative and concrete

    Without this patch applied the example commit message in the CONTRIBUTING
    document is not a concrete example.  This is a problem because the
    contributor is left to imagine what the commit message should look like
    based on a description rather than an example.  This patch fixes the
    problem by making the example concrete and imperative.

    The first line is a real life imperative statement with a ticket number
    from our issue tracker.  The body describes the behavior without the patch,
    why this is a problem, and how the patch fixes the problem when applied.
```

### Formatting Guidelines

In order to keep a sane source repository, we must ensure that the code remains
formatted in the same fashion. This becomes all the more important given
Python's requirement for sane formatting and indentation of source.

* Indents are added using 4 spaces.
  * Remember 4 spaces, not a tab character. Please ask your IDE to expand tabs
    to spaces.
* As far as possible, try to avoid CamelCase. We prefer the use of underscored
  variable names.
* The code should not exceed 80 characters in one line. If you need more, split
  the line into two.
  * When splitting the line, try to adhere to the guidelines provided by PEP8.
* Overall, we expect all code to adhere to PEP8 guidelines. You can use PEP8
  checkers to ensure that.

## Making Trivial Changes

### Documentation

For changes of a trivial nature to comments and documentation, it is not
always necessary to create a new issue. In this case, it is
appropriate to start the first line of a commit with '(doc)' instead of
an issue number.

pyCourseSync uses Sphinx to automatically generate documentation from the source
code. Hence, completely documented source is an extremely important part of the
project.

```
    (doc) Add documentation commit example to CONTRIBUTING

    There is no example for contributing a documentation commit
    to pyCourseSync. This is a problem because the contributor
    is left to assume how a commit of this nature may appear.

    The first line is a real life imperative statement with '(doc)' in
    place of what would have been the issue number in a
    non-documentation related commit. The body describes the nature of
    the new documentation or comments added.
```

## Submitting Changes

* Push your changes to a topic branch in your fork of the repository.
* Submit a pull request to the parent repository.

# Additional Resources

* [General GitHub documentation](http://help.github.com/)
* [GitHub pull request documentation](http://help.github.com/send-pull-requests/)
