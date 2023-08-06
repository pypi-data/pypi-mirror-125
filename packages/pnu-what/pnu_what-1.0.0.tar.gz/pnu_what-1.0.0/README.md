# Installation
pip install [pnu-what](https://pypi.org/project/pnu-what/)

# WHAT(1)

## NAME
what - identify SCCS keyword strings in files

## SYNOPSIS
**what**
\[-qs\]
\[--debug\]
\[--help|-?\]
\[--version\]
\[--\]
\[file ...\]

## DESCRIPTION
The **what** utility searches each specified file for sequences of the form "@(#)" as inserted by the SCCS source code control system.
It prints the remainder of the string following this marker, up to a NUL character, newline, double quote, ‘>’ character, or backslash.

### OPTIONS
The following options are available:

Options | Use
------- | ---
-q|Only output the match text, rather than formatting it
-s|Stop searching each file after the first match
--debug|Enable debug mode
--help\|-?|Print usage and a short help message and exit
--version|Print version and exit
--|Options processing terminator

## ENVIRONMENT
The *WHAT_DEBUG* environment variable can be set to any value to enable debug mode.

The *FLAVOUR* or *WHAT_FLAVOUR* environment variables can be set to one of the following values, to implement only the corresponding options and behaviours.
* posix : POSIX [what](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/what.html)
* bsd | bsd:freebsd : FreeBSD [what(1)](https://www.freebsd.org/cgi/man.cgi?query=what)
* linux : Linux [what(1P)](https://man7.org/linux/man-pages/man1/what.1p.html)

However, if the *POSIXLY_CORRECT* environment variable is set to any value, then the POSIX flavour will be selected.

## EXIT STATUS
Exit status is 0 if any matches were found, otherwise 1.

## SEE ALSO
[ident(1)](https://github.com/HubTou/ident/blob/main/README.md),
[strings(1)](https://github.com/HubTou/strings/blob/main/STRINGS.1.md)

## STANDARDS
The **what** utility is a standard UNIX/POSIX command.

It conforms to IEEE Std 1003.1-2001 (“[POSIX.1](https://en.wikipedia.org/wiki/POSIX)”).
The *-q* option is a non-standard [FreeBSD](https://www.freebsd.org/) extension which may not be available on other operating systems.

This re-implementation tries to follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for [Python](https://www.python.org/) code.

## PORTABILITY
Tested OK under Windows.

## HISTORY
The **what** command appeared in [UNIX Programmer's Workbench (PWB/UNIX)](https://en.wikipedia.org/wiki/PWB/UNIX) 1.0 in 1977,
and was probably written by [Marc J. Rochkind](https://en.wikipedia.org/wiki/Marc_Rochkind) along with the rest of the [Source Code Control System (SCCS)](https://en.wikipedia.org/wiki/Source_Code_Control_System).

The [BSD](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution) version appeared in [4.0BSD](https://en.wikipedia.org/wiki/History_of_the_Berkeley_Software_Distribution#4BSD) in October 1980 and was rewritten because SCCS was not licensed with [Version 32V AT&T UNIX](https://en.wikipedia.org/wiki/UNIX/32V).

This re-implementation was made for the [PNU project](https://github.com/HubTou/PNU).

## LICENSE
It is available under the [3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).

## AUTHORS
[Hubert Tournier](https://github.com/HubTou)

This manual page is based on the one written for [FreeBSD](https://www.freebsd.org/).

