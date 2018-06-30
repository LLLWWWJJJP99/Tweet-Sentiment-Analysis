import tweepy
import socket, re
import googlemaps

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""


class MyScraper(tweepy.StreamListener):

    def __init__(self, conn=None):
        self.conn = conn
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        self.gmaps = googlemaps.Client(key='AIzaSyAxEtQaX4yhn8dZfZQp9LQjW3noMB4iaRw')

    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            print(status_code)

    def on_status(self, status):
        '''
        Setup a listener to accept new tweets. Store content of each tweet and fetch coordinate of
        location of user in text using google map geocoding API, then sent text to spark streaming.
        Here I use '|' to seperate each tweet, which would used to restore the real physical meaning tweets.
        :param status:
        :return:
        '''
        # remove invalid emoji and symbols
        text = re.sub(r'[^\w.\s#@/:%,_-]', "", status.text)
        if status.user.location:
            geo = self.gmaps.geocode(status.user.location)
            if geo:
                coordinate = geo[0]['geometry']['location']
                location = str(coordinate['lng']) + "," + str(coordinate['lat'])
            else:
                location = ''
        else:
            location = ''

        text = '|(' + location + ')' + text + '|'
        print('===================')
        print(text)
        print('===================')
        conn.send(text.encode('utf-8'))


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 50010))
    s.listen(1)
    conn, addr = s.accept()

    scraper = MyScraper(conn)
    # scraper = MyScraper()
    myStream = tweepy.Stream(auth=scraper.auth, listener=scraper)
    # only fetch english tweets which use trump and obama as hashtag
    myStream.filter(languages=['en'], track=['#Trump', '#Obama'])
