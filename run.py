import os
from app import app
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="MEMEX EXPLORER")

    parser.add_argument("-s", "--show", action="store_true",
                        help="Auto-raise app in a browser window")

    return parser.parse_args()

app.config.from_pyfile('config.py')

if __name__ == "__main__":
    args = parse_args()


    if args.show:
        url = "http://%s:%s/" % (app.config['HOST'], app.config['PORT'])
        if app.config['DEBUG']:
            print url
        else:
            import webbrowser
            webbrowser.open(url)

    if not app.debug:
        import logging
        file_handler = logging.FileHandler('memex_explorer.log')
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
