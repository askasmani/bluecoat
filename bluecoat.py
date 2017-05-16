import sys
import fileinput
import requests
import json
from bs4 import BeautifulSoup

# perform a lookup of the site against Bluecoat and return the current category
# note: Bluecoat will rate-limit you if there are lots of requests.
class SiteReview(object):
    def __init__(self):
        self.baseurl = "http://sitereview.bluecoat.com/rest/categorization"
        self.useragent = {"User-Agent": "Mozilla/5.0"}

    def sitereview(self, url):
        payload = {"url": url}
        
        try:
            self.req = requests.post(self.baseurl,headers=self.useragent,data=payload)
        except requests.ConnectionError:
            sys.exit("[-] ConnectionError: A connection error occurred")

        return json.loads(self.req.content)


def main(argv):
    inputfile = ''
    # ensure correct usage
    if len(sys.argv) < 2:
        print "Usage : " + sys.argv[0] + " <inputfile>"
        sys.exit(1)
    else:
        inputfile = sys.argv[1]

    # iterate each line in the input file
    for line in fileinput.input([inputfile]):
        url = line.rstrip('\n')
        # use try, except pass to skip over any errors
        try:
            s = SiteReview()
            response = s.sitereview(url)
            # print response
            cat = BeautifulSoup(response["categorization"], "lxml").get_text()
            print url, "-->", "["+cat+"]"
        except:
            print "Skipping over " + line
            pass

if __name__ == "__main__":
    main(sys.argv[1:])