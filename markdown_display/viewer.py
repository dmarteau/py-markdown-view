""" Simple markdown viewer as http server
"""
import os
import mimetypes
from markdown import markdown
from bottle import route, static_file, abort, request, run
from urllib.parse import urlparse

MARKDOWN_EXTS = ('.md','.markdown','.mdown','mkdn', 'mdwn', 'mkd')

script_dir = os.path.dirname(os.path.realpath(__file__))

HTML_HEAD="""
<!DOCTYPE html>
<html>
<head>
    <title>{path}</title>
    <link href="/css/markdown.css" rel="stylesheet">
    <link href="/css/pygments.css" rel="stylesheet">
</head>
<body style="background-color: white;">
<div class="html-output markdown-body" id="html_result" style="overflow: auto; height:100%">
"""

HTML_FOOT="""
</div>
</body>
</html>
"""

def serve_files(path):
    """ Return either a directory listing
    """
    if os.path.isdir(path):
        # List directory
        host  = request.get_header('host')
        rpath = '' if path == '.' else path+'/'
        tpl   = '<a href="http://{0}/files/{1}{{0}}">{{0}}</a><br/>'.format(host,rpath)
        return ('\n').join(tpl.format(s) for s in os.listdir(path))
    if os.path.isfile(path):
        _,ext = os.path.splitext(path)
        if ext.lower() in MARKDOWN_EXTS:
            # Convert markdown to HTML
            with open(path,'r') as fp:
                html = markdown(fp.read())
            return HTML_HEAD.format(path=path) + html + HTML_FOOT    
        else:
            # Return static file
            filename = os.path.basename(path)
            rootdir  = os.path.abspath(os.path.dirname(path))
            mimetype = mimetypes.types_map.get(ext)
            return static_file(os.path.basename(path),root=rootdir, mimetype=mimetype)
    else:
        abort(404, "The path '%s' does not exists" % path)

@route('/')
def route_handler():
    host  = request.get_header('host')
    return '<form><button formaction="http://{0}/close">Close</button></form>'.format(host)


@route('/close')
def close_handler():
    """ Kill ourselve with SIGTERM
    """
    import  signal
    os.kill(os.getpid(), signal.SIGTERM)


@route('/css/<path:path>')
def style_handler(path):
    return static_file(path,os.path.join(script_dir, 'css'))


@route('/files/')
@route('/files/<path:path>')
def path_handler(path='.'):
    return serve_files(path)


def main():
    import argparse
    import webbrowser

    p = argparse.ArgumentParser(description="Simple markdown viewer")
    p.add_argument('-p','--port' , type=int, default=1357, help="http port", dest='port')
    p.add_argument('-i','--iface', default='localhost', help="interface", dest='iface')
    p.add_argument('file' , default='', nargs='?', help="File to open")
    args = p.parse_args()

    import webbrowser
    webbrowser.open('http://{}:{}/files/{}'.format(args.iface, args.port, args.file))

    try:
        run(host=args.iface,port=args.port) 
    except OSError as e:
        if e.errno == 98:
            pass

