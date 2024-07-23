from playwright.sync_api import sync_playwright

def scrape(url:str) -> dict:
    ###
    # Scrape a single tweet page for tweet thread. Return parent tweet, reply tweets and reccomended tweets
    
    ###

    #xhr: background requests
    _xhr_calls =[]    

    def intercept_response(response):
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width":1920, "height":1080})
        page = context.new_page()

        #enable background request intercepting:
        page.on("response", intercept_response)
        #go to url and wait for the page to load
        page.goto(url)
        page.wait_for_selector("[data-testid='tweet']")

        #find all tweet background requests:
        tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
        for xhr in tweet_calls:
            data = xhr.json()
            return data['data']['tweetResult']['result']
    
if __name__ == "__main__":
    print(scrape("https://twitter.com/Scrapfly_dev/status/1664267318053179398"))

