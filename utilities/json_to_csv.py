"""
Preprocess JSON Tweets files to CSV files with a subset of the fields
"""
import json
import csv
import cStringIO
import codecs
import os
import string


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
 

def tweets_to_csv(infile_path):
    """Converts Streaming JSON Tweets to CSV with a subset of the fields.

    Args:
        infile_path (str) : path to folder containing the json files stored from the Twitter Streaming API.

    Returns:
        A CSV file containing the following tweet fields: 'id','user_id', 'user_name', 'user_screen_name', 'timestamp', 
        'text', 'lang', 'retweet_count', 'favorite_count', 'links_url', 'media_url', 'longitude', 'latitude'.

    .. note:: For more information visit `Twitter REST API <https://dev.twitter.com/overview/api/tweets>`_.
    """  
    outfile_path = infile_path.replace('json', 'tsv')
    if outfile_path == infile_path:
        raise Exception(outfile_path, 'Input and Output files are the same, :(')
    with open(outfile_path, 'w') as f:
        writer = UnicodeWriter(f)
        #create a list with headings for our columns (problems with headers)
        headers = ['id','user_id', 'user_name', 'user_screen_name', 'timestamp', 'text', 'lang', 'retweet_count', 'favorite_count', \
                    'links_url', 'media_url', 'longitude', 'latitude']
         
        #write the row of headings to our CSV file
        writer.writerow(headers)
         
        reader = open(infile_path, 'rb')
        #run through each item in results, and jump to an item in that dictionary, ex: the text of the tweet
        for line in reader.readlines():
            #initialize the row
            row = []
            tweet = json.loads(line)
            #add every 'cell' to the row list, identifying the item just like an index in a list
            row.append(tweet['id_str'])
            row.append(tweet['user']['id_str'])
            row.append(tweet['user']['name'])
            row.append(tweet['user']['screen_name'])
            row.append(tweet['timestamp_ms'])
            row.append(tweet['text'])
            row.append(tweet['lang'])
            row.append(str(tweet['retweet_count']))
            row.append(str(tweet['favorite_count']))
            if tweet['entities']['urls']:
                row.append(tweet['entities']['urls'][0]['url']) 
            else:
                row.append('')
            if 'media' in tweet['entities']:
                media_url = tweet['entities']['media'][0]['media_url']
            else:
                media_url = ""
            row.append(media_url)
            if tweet['coordinates']:
                longitude = str(tweet['coordinates']['coordinates'][0])
                latitude = str(tweet['coordinates']['coordinates'][1])
            else:
                latitude = ''
                longitude = ''
            row.append(longitude)
            row.append(latitude)

            #once you have all the cells in there, write the row to your csv
            writer.writerow(row)

        reader.close()

data_dir = '/Users/cdoig/Desktop/ebola-twitter/data/'
for f in os.listdir(data_dir):
    if f.endswith(".json"):
        tweets_to_csv(data_dir + f)

