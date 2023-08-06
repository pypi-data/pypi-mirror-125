# scons-tool-bennugd

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[SCons](https://scons.org/doc/production/HTML/scons-user.html) tool to build
[BennuGD](https://bennugd.org) projects.

## Installation

There are a few ways to install this tool for your SCons project.

### From [pypi](https://pypi.org/)

This method may be preferable if you build your project under a virtualenv. To
add a `scons-tool-bennugd` from pypi, type (within your virtualenv):

```
pip install scons-tool-bennugd
```

Or, if your project uses [pipenv](https://pipenv.readthedocs.io/):

```
pipenv install --dev scons-tool-bennugd
```

Alternatively, you may add this to your `Pipfile`:

```
[dev-packages]
scons-tool-bennugd = "*"
```

The tool will be installed as a namespaced package `sconstool.bennugd` in the
project's virtual environment.

### As a git submodule

In your git repository, add the `scons-tool-bennugd` as a submodule:

```
git submodule add git://bitbucket.org/dacucar/scons-tool-bennugd.git
```

### Manually downloading  `dcbc` module

Download the `dcbc` tool module into the `site_scons/site_tools`. 

```bash
mkdir -p site_scons/site_tools
curl https://bitbucket.org/dacucar/scons-tool-bennugd/raw/HEAD/sconstool/bennugd/dcbc.py -o site_scons/site_tools/dcbc.py 
```

## Usage example

First, create your game sources:

```
game/
│
└───lib/
│   │   lib.prg
|   |   lib.h
│
└───game/
│   │   game.prg
│   │   game_part_1.prg
|   |   ...
│
└───tool/
    │   tool.prg
    │   tool_part_1.prg
    |   ...
```

In this example, `tool` and `game` depend on `lib`. Also `game_part_1.prg`
is included in `game.prg` and `tool_part_1.prg` is included in `tool.prg`.

Then, write SConstruct file.

```python
# SConstruct
env = Environment(
	# We need to tell scons how to find the tool package...
	# ...if you installed it with pip/pipenv use
	toolpath = [PyPackageDir('sconstool.bennugd')],
	# ... OR if you installed it as a git submodule
	# toolpath = ['scons-tool-bennugd/sconstool/bennugd']
	# ... OR if you downloaded the dcbc.py into site_scons/site_tools, then there is no need to specify toolpath

	tools = ['default', 'dcbc']
	)

# Declare three targets
env.Dcl('lib.dcl', 'lib/lib.prg')
env.Dcb('game.dcb', 'game/game.prg', DCBCLIBS='lib/lib.dcl')
env.Dcb('tool.dcb', 'game/tool.prg', DCBCLIBS='lib/lib.dcl')
```

> __TIPS__
>
> The extension of the targets and source files can be omitted.

Finally, try it out.

To build all targets:

```
scons
```

To clean:

```
scons -c
```

To build only `game` target:

```
scons game
```

You may want to check the [Example](https://bitbucket.org/dacucar/scons-tool-bennugd/src/master/sconstool/).

SCons is a very feature rich build-system and highly customizable.

## It can also be used with [PixTudio](https://pixtudio.org)!

The variable `DCBC` allows defining the DCB compiler, which can be set to
`pxtb`.

```python
env = Environment(
	toolpath = [PyPackageDir('sconstool.bennugd')],
	tools = ['default', 'dcbc'],
	DCBC = 'pxtb'
	)
```

## Supported Options

The following options are accepted by the `Dcl` and the `Dcb` builders:

| Variable | Default | Description |
| --- | --- | --- |
| DCBC | `"bgdc"` | DCB compiler. |
| DCBCFLAGS | `""` | Additional compilation flags. |
| DCBCMACROS | `{}` | Additional compilation macros, expressed as a dictionary. |
| DCBCPATH | `[]` | Additional paths where the compiler shall search for files. |
| DCBCFILES | `[]` | A list of files that shall be added to the dcb. |
| DCBCLIBS | `[]` | A list of libraries that shall be included by the compiler. |
| DCBCLIBEXTENSION | `".dcl"` | The extension used when compiling in _libmode_. |
