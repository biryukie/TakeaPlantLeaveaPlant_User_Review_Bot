# /r/TakeaPlantLeaveaPlant User Review Bot
A user review bot for /r/TakeaPlantLeaveaPlant.

The bot takes three arguments in the form of `username rating review_URL`, adds the user to a wikipage for reviews starting with their username's first character, and updates their flair.

## Requirements
1. Install [Python 3.6.8](https://www.python.org/downloads/release/python-368/)
2. Install [PRAW](https://praw.readthedocs.io/en/latest/getting_started/installation.html)

### Reddit Configuration
1. [Create a new Reddit app](https://reddit.com/prefs/apps)
   1. Select `script` type app
   2. `redirect uri` can be something like `http://localhost:8080`
2. Note the `personal use script` and the `secret` values

## Usage
### Authentication
This app uses basic ["Password Flow" authentication](https://praw.readthedocs.io/en/latest/getting_started/authentication.html#password-flow), meaning you need a text file located on your computer with the following four values on separate lines:
* client id (`personal use script`)
* client secret (`secret`)
* your bot account's username
* your bot account's password

The `loc.txt` in the code on line `credentials = open(open("loc.txt", "r").readline().strip(), "r")` has the location of the text file with my credentials. If you wish to have your credentials file in the same location as the application, change this line to `credentials = open("YOUR_CREDENTIALS_FILE.txt", "r")`

### Set Up
* Line `THE_FILE = "NAME.txt"` near the top can be changed to whatever you want your temporary local version of your wikipage to be. 
* In `main()` modify `sub = reddit.subreddit("YOUR_SUBREDDIT_NAME")` and `page = sub.wiki["YOUR_REVIEWS_WIKI_PAGE"]`
* I haven't tested what happens if you don't have the wiki pages for each character already set up. You may want to set up the wiki pages before hand. 

### Program Execution
When running the program, you will be prompted to enter a string consisting of `username rating review_URL`. Once this is entered, the review wiki page gets updated and the user's flair is calculated and set. 
