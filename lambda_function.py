import tweepy, random, os, time
from creds import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def post_tweet(tweetContent):
    api.update_status(tweetContent)
    term_size = os.get_terminal_size()
    print('-' * term_size.columns)
    print('TWEETED : ', tweetContent)
    term_size = os.get_terminal_size()
    print('-' * term_size.columns)
    

def upload_media(text, filename):
    media = api.media_upload(filename)
    api.update_status(text, media_ids = [media.media_id_string])

def updateBooks(selectedQuote, tweetBookFile):
    
    os.chdir('tweeted')
    with open(tweetBookFile, 'a+') as f:
        f.write(selectedQuote)
    print('Updated books in the tweeted directory')


def chooseRndBook():
    os.chdir("sources") #the folder name which has the .txt files
    dir = os.getcwd()
    bookSet = os.listdir(dir)
    try:
        bookSet.remove('.DS_Store')
    except:
        pass
    #to randomly choose a book from the directory
    selectedBookFile = random.choice(bookSet)
    return selectedBookFile

#to chooose random Quote from a book
def getRndQuote (selectedBookFile):

    with open(selectedBookFile, 'r+') as f:

        bookContent = f.read()
        quoteList = bookContent.split('$') #makes a list with eacuj element marked by $ at the end
        selectedQuote = random.choice(quoteList)
        print('The selected quote is :', selectedQuote, 'from the book', selectedBookFile)

        #removes the selectedQuote from the list so it may not be tweeted again in future
        quoteList.pop(quoteList.index(selectedQuote))
        #to rewrite the file with the selectedQuote removed
        f.seek(0)                  
        f.truncate()
        f.writelines(quoteList)

        updateBooks(selectedQuote, selectedBookFile)
    return selectedQuote

def getQuote():
    return getRndQuote(chooseRndBook())

def lambda_handler(event, context):

    selectedQuote = getQuote()
    

    print(f"Post tweet: {selectedQuote}")
    post_tweet(selectedQuote) 

    return {"statusCode": 200, "tweet": selectedQuote}
