# cadcorp-pysis-startup

Startup script for Python in
[Cadcorp SIS Desktop](https://www.cadcorp.com/products/desktop/) 8.0 or later.

It is used as a regular
[PYTHONSTARTUP](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONSTARTUP)
script for the embedded Python command line in Cadcorp SIS Desktop.

It can contain definitions of convenient utilities, classes and functions,
as well as commands executed at startup to carry out repetitive operations.

## Installation

1. Launch Cadcorp SIS Desktop 8.0 or later
2. Go to File > Options > Python
3. Set `PYTHONSTARTUP` path to location of the `startup.py`.
4. Re-launch Cadcorp SIS Desktop.

For more details, check the Cadcorp SIS Desktop documentation about
[Options command](https://help.cadcorp.com/en/8.0/sis/help/#Commands_AComPreferences.html?Highlight=PYTHONSTARTUP).

## Quickstart

```
dir()               # List names, including startup.py ones
sis_help(sis_help)  # Learn about sis_help() function
```

## License

This is free and unencumbered software released into the public domain.

For more information, please refer to <http://unlicense.org>
