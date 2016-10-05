# bepasty-client

This is a command line client for [bepasty](https://github.com/bepasty/bepasty-server), a self-hostable binary pastebin.

There is already a prior, official, working command line client implementation available
[here](https://github.com/bepasty/bepasty-client-cli) - please use it!

`bepasty-client` was mostly written due to my frustration with a client that works only with older library versions and
the ridiculously old Python 2 - so I went and wrote a client that only works with the ridiculously new (Beta 1 as of
the time of this writing) Python 3.6.

## Status

 - [x] pastebin listing
 - [x] file upload
 - [x] stdin upload
 - [ ] file download
 - [ ] copy url to clipboard after upload
 - [ ] file deletion (once exposed in bepasty)
 - [ ] interactive shell
 - [ ] tests
