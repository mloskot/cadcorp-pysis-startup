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

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
