# Simple markdown viewer server

Very stupid simple markdown viewer server.

Usage:

```
markdown-display [-p PORT] [-i IFACE] [file]
```

Port default to `2222` and iface to `localhost`.

Example:

```
markdown-display README.md
```

Will open README.md in your browser.

* Support opening multiple file with the same instance 
* Based on [Bottle](https://bottlepy.org/docs/dev/) and [Markdown](https://python-markdown.github.io/)


### Why ?

Because I was pissed off to not beeing able to simply display local markdown files in Firefox since 
web extensions cannot access local.  Also, I don't care about editing or other bells and whistles.


