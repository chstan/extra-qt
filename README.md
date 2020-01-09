# extra-qt 

[![Build Status](https://dev.azure.com/chstansbury/extra-qt/_apis/build/status/chstan.extra-qt?branchName=master)](https://dev.azure.com/chstansbury/extra-qt/_build/latest?definitionId=2&branchName=master)
[![Docs Status](https://readthedocs.org/projects/extra-qt/badge/?version=latest&style=flat)](https://extra-qt.readthedocs.io/en/latest/)
[![Coverage Status](https://img.shields.io/azure-devops/coverage/chstansbury/extra-qt/2.svg)](https://dev.azure.com/chstansbury/extra-qt/_build?definitionId=2)

## What is `extra_qt`?

![Example](docs/source/_static/basic_example.gif "Live Reload Example")

`extra_qt` is a view layer for Python around PyQt5.
It aims to be roughly interface comparable to React in Javascript.
As a result, you can declare `Component` classes with the same lifecycle
methods as in React:

* `before_mount`
* `after_mount`
* `before_receive_props`
* `should_update`
* `before_unmount`

Unlike React Native, QML, or React QML, `extra_qt`
is written entirely in Python so there's no bundled
JavaScript interpreter, and working with it should be simpler
for Python programmers.

The current (alpha) version of `extra_qt` works around a
fairly literal (and primitive) version of the
[React Stack Reconciler](https://reactjs.org/docs/implementation-notes.html), 
with some terminology differences. As a result, `extra_qt` is considered 
pre-release and is distributed with a copy of the React license.

Have a look at the examples folder to see what UI
scripting looks like. For those coming from React, keep in mind there's no
syntactic sugar like that provided by JSX for the moment.

To play with the examples, install [watchgod](https://github.com/samuelcolvin/watchgod) 
or another code reload tool and run

```bash
$> watchgod examples.basic.main
or
$> watchgod examples.nested_components.main
```

## Limitations

The diff algorithm (reconciler) is currently very primitive. In
particular, there is no support for:

1. keys
2. batched updates
3. `None`/missing children

Additionally, at the view layer, there is no support for bare string or `list` returns
from Components.

## Why not use bare PyQt5?

PyQt5 doesn't provide the most... convenient... bindings from a Python perspective.
Writing custom widgets and composing them is also less than fun due to the cumbersome
layout interface.

The Component structure also enforces more reasonable architecture than might otherwise
emerge in a standard PyQt utility, which is as important as convenience.

## Isn't this slow?

It's fast enough for relatively complex applications and UI scripting. In an ideal world
we might have a view layer similar to React for native applications with FFI bindings to
many different languages and targets. We'll get there.



