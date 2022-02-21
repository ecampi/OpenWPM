from pathlib import Path

from custom_command import LinkCountingCommand
from openwpm.command_sequence import CommandSequence
from openwpm.commands.browser_commands import GetCommand
from openwpm.config import BrowserParams, ManagerParams
from openwpm.storage.sql_provider import SQLiteStorageProvider
from openwpm.task_manager import TaskManager

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = [
   "google.com",
    "youtube.com",
    "facebook.com",
    "amazon.com",
    "yahoo.com",
    "wikipedia.org",
    "reddit.com",
    "pornhub.com",
    "walmart.com",
    "ebay.com",
    "twitter.com",
    "bing.com",
    "instagram.com",
    "fandom.com",
    "cnn.com",
    "xvideos.com",
    "espn.com",
    "pinterest.com",
    "xhamster.com",
    "foxnews.com",
    "twitch.tv",
    "live.com",
    "craigslist.org",
    "usps.com",
    "target.com",
    "netflix.com",
    "microsoftonline.com",
    "xnxx.com",
    "weather.com",
    "imdb.com",
    "accuweather.com",
    "ups.com",
    "zillow.com",
    "paypal.com",
    "etsy.com",
    "bestbuy.com",
    "msn.com",
    "duckduckgo.com",
    "office.com",
    "nytimes.com",
    "homedepot.com",
    "linkedin.com",
    "onlyfans.com",
    "quora.com",
    "spankbang.com",
    "indeed.com",
    "tiktok.com",
    "kohls.com",
    "microsoft.com",
    "lowes.com",
    "fedex.com",
    "aol.com",
    "walgreens.com",
    "instructure.com",
    "cvs.com",
    "t-mobile.com",
    "att.com",
    "chase.com",
    "amazonaws.com",
    "zoom.us",
    "outbrain.com",
    "healthline.com",
    "tynt.com",
    "quizlet.com",
    "xfinity.com",
    "realtor.com",
    "jivox.com",
    "taboola.com",
    "cheatsheet.com",
    "chaturbate.com",
    "macys.com",
    "samsung.com",
    "blogspot.com",
    "washingtonpost.com",
    "discord.com",
    "nypost.com",
    "criteo.net
    "apple.com",
    "cnbc.com",
    "webmd.com",
    "allrecipes.com",
    "wellsfargo.com",
    "yelp.com",
    "hulu.com",
    "imgur.com",
    "capitalone.com",
    "narvar.com",
    "costco.com",
    "weather.gov
    "stackoverflow.com",
    "usablenet.com",
    "github.com",
    "bankofamerica.com",
    "nextdoor.com",
    "roblox.com",
    "dailymail.co.uk",
    "archiveofourown.org",
    "steamcommunity.com",
    "npr.org",
    "ibighit.com"
]

# Loads the default ManagerParams
# and NUM_BROWSERS copies of the default BrowserParams

manager_params = ManagerParams(num_browsers=NUM_BROWSERS)
browser_params = [BrowserParams(display_mode="headless") for _ in range(NUM_BROWSERS)]

# Update browser configuration (use this for per-browser settings)
for browser_param in browser_params:
    # Record HTTP Requests and Responses
    browser_param.http_instrument = True
    # Record cookie changes
    browser_param.cookie_instrument = True
    # Record Navigations
    browser_param.navigation_instrument = True
    # Record JS Web API calls
    browser_param.js_instrument = True
    # Record the callstack of all WebRequests made
    browser_param.callstack_instrument = True
    # Record DNS resolution
    browser_param.dns_instrument = True

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params.data_directory = Path("./datadir/")
manager_params.log_path = Path("./datadir/openwpm.log")

# memory_watchdog and process_watchdog are useful for large scale cloud crawls.
# Please refer to docs/Configuration.md#platform-configuration-options for more information
# manager_params.memory_watchdog = True
# manager_params.process_watchdog = True


# Commands time out by default after 60 seconds
with TaskManager(
    manager_params,
    browser_params,
    SQLiteStorageProvider(Path("./datadir/crawl-data.sqlite")),
    None,
) as manager:
    # Visits the sites
    for index, site in enumerate(sites):

        def callback(success: bool, val: str = site) -> None:
            print(
                f"CommandSequence for {val} ran {'successfully' if success else 'unsuccessfully'}"
            )

        # Parallelize sites over all number of browsers set above.
        command_sequence = CommandSequence(
            site,
            site_rank=index,
            callback=callback,
        )

        # Start by visiting the page
        command_sequence.append_command(GetCommand(url=site, sleep=3), timeout=60)
        # Have a look at custom_command.py to see how to implement your own command
        command_sequence.append_command(LinkCountingCommand())

        # Run commands across all browsers (simple parallelization)
        manager.execute_command_sequence(command_sequence)
