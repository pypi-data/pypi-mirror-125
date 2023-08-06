import bs4
import feedparser
from json_database import JsonStorageXDG

try:
    import praw
except ImportError:
    praw = None


class RedditMediaFinder:
    def __init__(self, client=None, secret=None,
                 user_agent="RedditMediaFinder",
                 subs=None, blacklist=None, db_name="reddit_yt_movies"):
        self.reddit = None
        if client and secret:
            self.authenticate(client, secret, user_agent)
        self.subs = subs or []
        self.blacklist = blacklist or ["Deleted video", "trailer"]
        self.db = JsonStorageXDG(db_name)

    def authenticate(self, client, secret, user_agent):
        if praw:
            self.reddit = praw.Reddit(
                client_id=client,
                client_secret=secret,
                user_agent=user_agent
            )

    def _parse_submission_praw(self, submission):
        try:
            data = submission.secure_media["oembed"]
            soup = bs4.BeautifulSoup(data["html"], "html.parser")
            url = soup.find("iframe")["src"].split("?")[0] \
                .replace("https://www.youtube.com/embed/",
                         "https://www.youtube.com/watch?v=")
            if any(k.lower() in data["title"].lower()
                   for k in self.blacklist):
                return None
            return {
                "title": data["title"],
                "channel_url": data["author_url"],
                "thumbnail": data["thumbnail_url"],
                "url": url
            }
        except:
            return None

    def _parse_sub_praw(self, sub, limit=None):
        movies = []
        for submission in self.reddit.subreddit(sub).rising(limit=limit):
            mov = self._parse_submission_praw(submission)
            if mov and mov not in movies:
                movies.append(mov)
                yield mov

        for submission in self.reddit.subreddit(sub).top(limit=limit):
            mov = self._parse_submission_praw(submission)
            if mov and mov not in movies:
                movies.append(mov)
                yield mov

        for submission in self.reddit.subreddit(sub).new(limit=limit):
            mov = self._parse_submission_praw(submission)
            if mov and mov not in movies:
                movies.append(mov)
                yield mov

        for submission in self.reddit.subreddit(sub).hot(limit=limit):
            mov = self._parse_submission_praw(submission)
            if mov and mov not in movies:
                yield mov

    def _parse_sub(self, sub):
        if self.reddit:
            for movie in self._parse_sub_praw(sub):
                yield movie
        else:
            # parse rss feed, no auth needed
            feed = feedparser.parse(f"https://www.reddit.com/r/{sub}.rss")
            for data in feed["entries"]:
                content = data["content"][0]["value"]
                soup = bs4.BeautifulSoup(content, "html.parser")
                for a in soup.find_all("a"):
                    if "watch?v=" in a["href"]:
                        yield {
                            "title": data["title"],
                            "url": a["href"]
                        }

    def scrap(self, max=0, store=True):
        count = 0
        for sub in self.subs:
            for movie in self._parse_sub(sub):
                yield movie
                self.cache_result(movie, sub, store=store)
                count += 1
                if max and count >= max:
                    return

    def cache_result(self, res, sub, store=False):
        if sub not in self.db:
            self.db[sub] = []
        if res not in self.db[sub]:
            self.db[sub].append(res)
            if store:
                self.db.store()


class RedditMovies(RedditMediaFinder):
    def __init__(self, client=None, secret=None,
                 user_agent="RedditMediaFinder"):
        super().__init__(client=client, secret=secret, user_agent=user_agent,
                         subs=["fullmoviesonyoutube",
                               "FullLengthFilms",
                               "FullSciFiMovies"],
                         blacklist=None,
                         db_name="reddit_yt_movies")

    def _parse_sub(self, submission):
        for data in super()._parse_sub(submission):
            if data:
                # clean up the title
                title = data["title"]
                for k in ["full HD movie", "Full movie"]:
                    title = title.replace(k, "") \
                        .replace(k.lower(), "") \
                        .replace(k.upper(), "") \
                        .replace(k.title(), "")
                title = title.lstrip("-").rstrip("-").strip()
                if "-" in title:
                    chnks = title.split("-")
                    if len(chnks) == 2:
                        title = chnks[0]
                        data["description"] = chnks[-1]
                data["title"] = title.strip()
                yield data


class RedditSciFiMovies(RedditMovies):
    def __init__(self, client=None, secret=None,
                 user_agent="RedditMediaFinder"):
        super().__init__(client, secret, user_agent)
        self.subs = ["FullSciFiMovies"]


class RedditDocumentaries(RedditMovies):
    def __init__(self, client=None, secret=None,
                 user_agent="RedditMediaFinder"):
        super().__init__(client, secret, user_agent)
        self.subs = ["Documentaries"]


class RedditCartoons(RedditMovies):
    def __init__(self, client=None, secret=None,
                 user_agent="RedditMediaFinder"):
        super().__init__(client, secret, user_agent)
        self.subs = ["fullcartoonsonyoutube"]


class RedditTVShows(RedditMovies):
    def __init__(self, client=None, secret=None,
                 user_agent="RedditMediaFinder"):
        super().__init__(client, secret, user_agent)
        self.subs = ["fulltvshowsonyoutube"]


if __name__ == "__main__":
    r = RedditSciFiMovies()
    for movie in r.scrap():
        print(movie)

    r = RedditMovies()
    for movie in r.scrap():
        print(movie)

    r = RedditCartoons()
    for movie in r.scrap():
        print(movie)

    r = RedditDocumentaries()
    for movie in r.scrap():
        print(movie)

    r = RedditTVShows()
    for movie in r.scrap():
        print(movie)
