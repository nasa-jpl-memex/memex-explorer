from __future__ import division

from bokeh.embed import autoload_server
from bokeh.session import Session
from bokeh.document import Document

GREEN = "#47a838"
DARK_GRAY = "#2e2e2e"
LIGHT_GRAY = "#6e6e6e"

from datetime import datetime, timedelta
import numpy as np
from bokeh.models import Range1d, FactorRange
from bokeh.plotting import figure, output_server, show

def load_data():
    f = open('/Users/aahmadia/nutch/nutch-python/wikipedia_example_data.log')
    data = f.readlines()

    def get_date(l):
        return np.datetime64(datetime.strptime(l.split(',')[0], '%Y-%m-%d %H:%M:%S'))

    def fetching_grabber(l):
        if 'fetcher.FetcherThread - fetching' in l:
            return l.partition('fetcher.FetcherThread - fetching ')[2].split()[0]

    def fetched_grabber(l):
        if 'TRACE api.HttpBase - fetched' in l:
            return l.partition(') from ')[2].split()[0]


    fetching = [(get_date(l), fetching_grabber(l)) for l in data if fetching_grabber(l)]
    fetched = [(get_date(l), fetched_grabber(l)) for l in data if fetching_grabber(l)]
    urls = [f[1] for f in fetching]
    x0 = [f[0] for f in fetching]
    url_ids = dict(zip(urls, range(len(urls))))
    x = [fetched[url_ids[f[1]]][0] for f in fetching]

    min_delta = np.timedelta64(timedelta(seconds=10))
    x = [max(xi0+min_delta, xi) for xi0, xi in zip(x, x0)]
    urls = [u.strip('https://').replace(':', '_').replace('-', '_')[:125] for u in urls]

    x0 = np.asarray(x0)
    x = np.asarray(x)
    urls = urls

    return x0, x, urls


def plot_server_stream():
    session = Session()
    document = Document()
    session.use_doc("wiki_crawl")
    session.load_document(document)
    x, x0, urls = load_data()

    if document.context.children:
        p1 = document.context.children[0]
    else:
        output_server("wiki_crawl")

        p1 = figure(title="Wikipedia Crawl", tools="resize,save,hover", y_range=urls, x_axis_type="datetime", width=800, height=400)
        min_x = min(x0)
        max_x = max(x[:5])
        x_range = Range1d(min_x, max_x)
        p1.x_range = x_range
        p1.x_range.start = min_x
        p1.x_range.end = max_x

        active_min = x0.searchsorted(min_x)
        active_max = x.searchsorted(max_x, side='right')

        active_x = x[active_min:active_max]
        active_x0 = x0[active_min:active_max]
        active_urls = urls[active_min:active_max]
        p1.y_range = FactorRange(factors=active_urls)

        p1.segment(active_x0, range(len(active_urls)), active_x, range(len(active_urls)), line_width=10, line_color="orange")
        p1.circle(active_x, range(len(active_urls)), size=5, fill_color="green", line_color="orange", line_width=12)

    document.add(p1)
    session.store_document(document)
    script = autoload_server(p1, session)

    #TODO: Looks like a Bokeh bug, probably not repeatable with current code
    script = script.replace("'modelid': u'", "'modelid': '")
    return script

