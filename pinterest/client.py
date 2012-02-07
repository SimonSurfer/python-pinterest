import urllib, urllib2

def ensure_access_token(f):
    def g(self, *args, **kwargs):
        if not self.access_token:
            raise PinterestException("You need an access token to make that call")
        f(self, *args, **kwargs)
    return g

class PinterestAPI(object):
    prefix_path = "https://api.pinterest.com/v2/"
    authorize_url = "https://api.pinterest.com/oauth/authorize"
    access_token_url = "https://api.pinterest.com/oauth/access_token"

    def __init__(self, access_token=None):
        self.access_token = access_token

    @ensure_access_token
    def _get_request(self, path, params={}):
        params["access_token"] = self.access_token
        url = "%s%s?%s" %(self.prefix_path, path, urllib.urlencode(params))
        try:
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError, err:
            raise PinterestException(err.read())
    
    def _post_request(self, path, params={}, data={}):
        params["access_token"] = self.access_token
        url = "%s%s?%s" %(self.prefix_path, path, urllib.urlencode(params))
        try:
            return urllib2.urlopen(url,urllib.urlencode(data)).read()
        except urllib2.HTTPError, err:
            raise PinterestException(err.read())

    def get_homefeed(self, page=1, limit=20):
        return self._get_request("home", {"page": page, "limit": limit})

    def get_pin(self, pin_id):
        return self._get_request("pin/%d" %(pin_id))
        
    def get_popular(self, page=1, limit=20):
        return self._get_request("popular", {"page": page, "limit": limit})
        
    def get_all(self, category="", page=1, limit=20):
        return self._get_request("all", {"category": category,"page": page, "limit": limit})

    def get_videos(self, page=1, limit=20):
        return self._get_request("videos", {"page": page, "limit": limit})
        
    def get_boards(self):
        return self._get_request("boards")
        
    def get_activity(self):
        return self._get_request("activity")
    
    #domain must be "pins","boards" or "people"
    def get_search(self, domain="pins", query=""):
        return self._get_request("search/%d" %(domain), {"query": query})
        
class PinterestException(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description

