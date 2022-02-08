
## v0.5.4
- include "template.html" in package data 

## v0.5.3
- line numbers
- separate stdout and stderr output blocks
- add block option to include files
- dont show  "#Block N" if stdout is empty
- PDF support
- Fix watch asset path when input not provided
## v0.5.2
- Add support for `rnuplot` - the root patched version of `gnuplot`
- load template html and css from files
- placeholder for args to override html and css templates
- make input optional so that input vs. watch is not confusing

## v0.5.1
- still trying to understand where to put data and how to include in package
- add yaml option to not render yaml frontmatter in output `hide: true`
- add more block options to replace comment versions
- add pygments highlighter option controlled by yaml frontmatter 

## v0.5.0
- move data into package, setup poetry to include it

## v0.4.0
- move data, but still in wrong place

## v0.3.0
- add block options
- add yaml front matter parser

## v0.2.0
- fix default css
- setup as package for submission to pypi as `rootmd`
- add `html`, `css`, and `js` output

## v0.1.0
- initial release
- basic functionality with Html and MD renderer + code execution