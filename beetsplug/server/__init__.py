from beets.plugins import BeetsPlugin
from beets import ui
import flask
import subprocess

# Flask setup.

app = flask.Flask(__name__)

@app.route('/')
def hello():
  return 'Hello World'

# returns 0 when completed - successful items or failed
# if file is in destination directory then good
@app.route('/tag')
def tag():
    if (app.config['import_log'] and app.config['tag_path']):
        import_log = app.config['import_log']
        tag_path = app.config['tag_path']
        import_cmd = subprocess.run(["beet", "import", "-ql", str(import_log), str(tag_path)])
        print("The exit code was %d" % import_cmd.returncode)
        return 'SUCCESS'    
    else:
        return 'FAIL'
    
    
    
    
    
    
    #os.system("./beet version")
    #subprocess.run(["./beet", "version"])
    #"import", "-ql", "/mnt/c/MusicNewTest/importlog.txt", "/mnt/c/MusicToTag_New"
    
    #list_files = subprocess.run(["ls", "-l"])
    #print("The exit code was: %d" % list_files.returncode)
    
    
    #os.system("./beet import -ql /mnt/c/MusicNewTest/importlog.txt /mnt/c/MusicToTag_New")
    
  
# Plugin hook.

class WebPlugin(BeetsPlugin):
    def __init__(self):
        super().__init__()
        self.config.add({
            'host': '127.0.0.1',
            'port': 8337,
            'cors': '',
            'cors_supports_credentials': False,
            'reverse_proxy': False,
            'include_paths': False,
            'readonly': True,
        })

    def commands(self):
        cmd = ui.Subcommand('server', help='start the server')
        cmd.parser.add_option('-d', '--debug', action='store_true',
                              default=False, help='debug mode')

        def func(lib, opts, args):
            args = ui.decargs(args)
            if args:
                self.config['host'] = args.pop(0)
            if args:
                self.config['port'] = int(args.pop(0))

            app.config['lib'] = lib
            # Normalizes json output
            app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

            app.config['INCLUDE_PATHS'] = self.config['include_paths']
            app.config['READONLY'] = self.config['readonly']
            
            if self.config['import_log']:
                app.config['import_log'] = self.config['import_log']
                
            if self.config['tag_path']:
                app.config['tag_path'] = self.config['tag_path']

            # Enable CORS if required.
            if self.config['cors']:
                self._log.info('Enabling CORS with origin: {0}',
                               self.config['cors'])
                from flask_cors import CORS
                app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
                app.config['CORS_RESOURCES'] = {
                    r"/*": {"origins": self.config['cors'].get(str)}
                }
                CORS(
                    app,
                    supports_credentials=self.config[
                        'cors_supports_credentials'
                    ].get(bool)
                )

            # Allow serving behind a reverse proxy
            if self.config['reverse_proxy']:
                app.wsgi_app = ReverseProxied(app.wsgi_app)

            # Start the web application.
            app.run(host=self.config['host'].as_str(),
                    port=self.config['port'].get(int),
                    debug=opts.debug, threaded=True)
        cmd.func = func
        return [cmd]
      
class ReverseProxied:
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    From: http://flask.pocoo.org/snippets/35/

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)
