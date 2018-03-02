# -*- coding: UTF-8 -*-
import twitter
import datetime
import googlemaps
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# ----------------------------------------------------------
# --------          HW 12: Twitter Search          ---------
# --------          Plus Geolocation Data          ---------
# ----------------------------------------------------------

# ----------------------------------------------------------
# Please answer these questions after having completed this
# program
# ----------------------------------------------------------
# Name: Nhiem Ngo
# Time spent on this program: 11 hours
# Collaborators and sources:
#   https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
# ----------------------------------------------------------



# ----------------------------------------------------------
# Fill in the following variables
# ----------------------------------------------------------
consumer_key = 'mRIXbupwGd19lr9QKCPkDnwFk' 
consumer_secret = 'g3y2xu7t5QBwDMJUDWrh0LTuRqwQP8jEnlZbn8H9inAwdnGt1f'
geocode_api_key = 'AIzaSyCXIwDuXhlNDh9cDk1sbFHtxevMqqOOGyg'

test_screen_name = 'colgateuniv'
test_address = '1600 Amphitheatre Parkway, Mountain View, CA'




# ----------------------------------------------------------
# Main Function for Testing
# ----------------------------------------------------------
def main():
    try:
        screen_name = 'colgateuniv'
        lat = '42.8166'
        long = '-75.5402'
        twitter_api = get_twitter_api()
        gmaps_client = get_gmaps_client()

##        #Tests for get_user():
##        print(get_user(twitter_api, 'colgateuniv'))
##        print(get_user(twitter_api, 'nintendo'))
##        print(get_user(twitter_api, 'fqf2f32f2'))

##        #Tests for get_tweets_by_user():
##        print(get_tweets_by_user(twitter_api, 'colgateuniv'))
##        print(get_tweets_by_user(twitter_api, 'nintendo'))
##        print(get_tweets_by_user(twitter_api, 'fqf2f32f2'))

##        #Tests for get_tweets_by_keyword():
##        print(get_tweets_by_keyword(twitter_api, "chainwax"))
##        print(get_tweets_by_keyword(twitter_api, "Alabama"))
##        print(get_tweets_by_keyword(twitter_api, 'fafwefwafw'))
##        print(get_tweets_by_keyword(twitter_api, ''))

##        #Test for get_trending_topics():
##        print(get_trending_topics(twitter_api))

##        #Test for get_trending_tweets():
##        print(get_trending_tweets(twitter_api))
##        #Test for get_trending_users():
##        print(get_trending_users(twitter_api))

##        #Tests for get_tweets_near_location():
##        print(get_tweets_near_location(twitter_api, 42.8183247, -75.5348576, "10mi"))
##        print(get_tweets_near_location(twitter_api, 48.864716, 2.349014, "20mi"))

##        #Tests for get_addr_from_cood():
##        print(get_addr_from_cood(gmaps_client, 42.8183247, -75.5348576))
##        print(get_addr_from_cood(gmaps_client, 48.864716, 2.349014))

##        #Tests for get_cood_from_addr():
##        print(get_cood_from_addr(gmaps_client, "McGregory Hall, Academic Dr, Hamilton, NY 13346, USA"))
##        print(get_cood_from_addr(gmaps_client, "18B Rue Tiquetonne, 75002 Paris, France"))

##        #Tests for get_place_name_from_cood()
##        print(get_place_name_from_cood(gmaps_client, '42.8183247', '-75.5348576'))
##        print(get_place_name_from_cood(gmaps_client, '48.864716', '2.349014'))

##        #Tests for get_place_name_from_addr() 
##        print(get_place_name_from_addr(gmaps_client, '1600 Amphitheatre Pkwy, Mountain View, CA 94043'))
##        print(get_place_name_from_addr(gmaps_client, 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France'))
##        print(get_place_name_from_addr(gmaps_client, '123 main st'))

##        #search() function test cases is located at the end of the file:
        
        
    except UnicodeEncodeError:
        print("This program cannot display emojis :(")
        
    
# ----------------------------------------------------------
# Write Your Code Here
# ----------------------------------------------------------

def tweet_to_string( status, location=False ):
    '''
    takes a twitter.status object representing a tweet
    returns that tweet as a string
    '''
    try:
        user = status.user.screen_name 
        date = tweet_date(status.created_at)
        tweet = status.text.replace("\n"," ")
        s = 'Tweet from @' + user + date + ': "' + tweet + '"'
        if location: # optionally append location name
            s += ' (' + status.place['full_name'] + ')'
        return s.translate(non_bmp_map) #avoid crashing when emojis appear
    except twitter.error.TwitterError as e:
        print('Error in status_to_string: ' + e + '\n')
        return False
    
def user_to_string(user):
    '''
    takes a twitter.user object representing a twitter user
    returns the user's information as a string
    '''
    # get the screen name, full name, and user description:
    screen_name = '@' + user.screen_name 
    name = user.name
    description = user.description
    s = screen_name + ' (' + name + ')' + ' "' + description + '"'
    return s.translate(non_bmp_map) #avoid crashing when emojis appear

def get_user( api, screen_name ):
    '''
     takes a twitter.api object and the screen name of a user as a string
     returns a twitter.user object representing that user
    '''
    try:
        user = api.GetUser(screen_name = screen_name)
        return user
    except twitter.error.TwitterError as e: #in case no user with the input screen_name is found
        return False


def get_tweets_by_user( api, screen_name ):
    '''
    takes a twitter.api object and the screen name of a user as a string
    returns a list of recent tweets (twitter.status objects) from the user’s timeline
    '''
    try:
        tweets = api.GetUserTimeline(screen_name = screen_name)
        return tweets
    except twitter.error.TwitterError as e: #in case no user with that name is found
        return False


def get_tweets_by_keyword( api, keyword ):
    '''
    takes a twitter.api object and a string
    returns a list of recent tweets (twitter.status objects) containing the given string
    '''
    try:
        result = []
        tweets = api.GetSearch(term = keyword) #use the GetSearch() method to get tweets relating to the keyword
        for tweet in tweets:
            if keyword in tweet.text:   #only get tweets where the keyword is in the content of the tweet
                result.append(tweet)
        return result
    except twitter.error.TwitterError as e: 
        return False

def get_trending_topics( api ):
    '''
    takes a twitter.api object
    returns a list of trending topics on twitter (as strings)
    '''
    result = []
    trends = api.GetTrendsCurrent()
    for trend in trends:
        result.append(trend.name) 
    return result

def get_trending_tweets( api ):
    '''
    takes a twitter.api object
    returns a dictionary where the keys are trending topics (strings) and the values are lists containing recent tweets (twitter.status objects) about that topic
    '''
    result = {}
    topics = get_trending_topics(api) #get trending topics first
    for topic in topics:
        result[topic] = api.GetSearch(term = topic) #create a dictionary entry with keys that are trending topics
    return result
    
def get_trending_users( api ):
    '''
    takes a twitter.api object and returns a dictionary where the keys are trending topics (strings) and
    the values are lists containing the users (twitter.user objects) who have recently tweeted about that topic
    '''
    result = {}
    user_list = []
    topics = get_trending_topics(api)   #get trending topics first
    for topic in topics:
        temp = api.GetSearch(term = topic)      #get statuses that talks about the trending topics
        for status in temp:
            user_list.append(status.user)       #get the poster of these statuses
        result[topic] = user_list   #add to the result
        user_list = []  
    return result

def get_tweets_near_location(api, lat, long, radius):
    '''
    takes a twitter.Api object, a latitude, a longitude, and the radius to search around those coordinates
    returns a list of twitter.Status objects containing recent tweets that were posted within that radius around the specified location
    '''
    tweets = api.GetSearch(geocode = (lat, long, radius))
    return tweets



# ----------------------------------------------------------
# New Location Functions

def get_addr_from_cood(client, lat, long):
    '''
    takes a googlemaps.Client object and the latitude and longitude of a location
    returns the closest address to that place as a string
    '''
    place = client.reverse_geocode(latlng = [lat, long])
    return place[0]['formatted_address'] #use the 'formatted_address key to easily get the address



def get_cood_from_addr(client, address):
    '''
    takes a googlemaps.Client object and a string containing the address of a location
    returns the coordinates of the place as a tuple (lat, long)
    '''
    place = client.geocode(address = address)
    if place != []: #prevent index error
        location = place[0]['geometry']['location'] #access the 'location' key inside the object
        return (location['lat'], location['lng'])
    else:
        return False

def get_place_name_from_cood(client, lat, long):
    '''
    takes a googlemaps.Client object and strings containing the latitude and longitude of a location 
    returns the name of that place as a string
    '''
    place = client.reverse_geocode(latlng = [lat, long])[0]
    if 'premise' in place['address_components'][0]['types']: #if the place actually has a name, return that name
        result = place['address_components'][0]['long_name']
    else:
        result = place['formatted_address']     #just return the address if the place does not have a name
    return result

def get_place_name_from_addr(client, address):
    '''
    takes a googlemaps.Client object and a string containing the address of a location
    returns the name of that place as a string
    if the name is not known, the address is returned
    '''
    if client.geocode(address = address) != []: #check if the address returns a valid result
        place = client.geocode(address = address)[0]    
        if 'premise' in place['address_components'][0]['types']: #check if the place has a name
            result = place['address_components'][0]['long_name']
        else:
            result = address    #return the address input if the place has no name
        return result
    else:
        return False

def get_tweet_place_name(api, tweet):
    return ""


    




# ----------------------------------------------------------
# Search Function

def search():
    ''' allows the user to search by username, keyword, or location '''
    twitter_api = get_twitter_api()
    gmaps_client = get_gmaps_client()
    answer = ''
    answer_user = ''
    result = ''
    while answer != '4':
        answer = input("\n\tHow would you like to search twitter?\n1. By username\n2. By keywords\n3. By location\n4. Exit\n")

        if answer == '1':
            print("\tSearch by username")
            while answer_user != '3':
                answer_user = input('\n1. Get information about a user\n2. Get tweets by a user\n3. Quit\n')
                if answer_user == '1' or answer_user == '2':
                    user_name = input('What is the username? ')
                    if answer_user == '1':
                        if get_user(twitter_api, user_name) == False:
                            result = "There is no user with this name"
                        else:
                            result = user_to_string(get_user(twitter_api, user_name))
                        print(result.translate(non_bmp_map)) #prevent error with displaying emoji
                    if answer_user == '2':
                        temp = get_tweets_by_user(twitter_api, user_name)
                        if temp == False:
                            result = "There is no user with this name"
                            print(result)
                        else:
                            result = temp
                            for t in result:
                                print(tweet_to_string(t))
                elif answer_user != '3':
                    print("Wrong input. Try again") 
                
        elif answer == '2':
            keyword = input("Input your keyword(s): ")
            tweets = get_tweets_by_keyword(twitter_api, keyword)
            if tweets == False or tweets == []:
                print("\nNo tweet found for \"" + keyword + "\"")
            else:
                print("\ntweets containing \"" + keyword + "\":")
                for tweet in tweets:
                    print(tweet_to_string(tweet))

        elif answer == '3':     #use get_cood_from_addr() and get_tweets_near_location() together to find results:
            place = input("\nYou can find trending tweets near a place. Where do you want to see trending tweets?\n")
            location = get_cood_from_addr(gmaps_client, place)
            if location != False:
                temp = get_tweets_near_location(twitter_api, location[0], location[1], "20mi")
                if temp != []:
                    print("\nSent near " + place + ":")
                    for tweet in temp:
                        print(tweet_to_string(tweet))
                else:
                    print("\nNo tweet was sent near", place)
        elif answer != '4':
            print("Invalid input. Try again")

    
    return None





# ----------------------------------------------------------
# Write Any Helper Functions Here
# ----------------------------------------------------------

def tweet_date( date_str ):
    try:
        date = datetime.datetime.strptime(date_str,
                                          '%a %b %d %H:%M:%S %z %Y')
        return date.strftime(' at %I:%M %p on %a %d, %Y')
    except Exception as e:
        print('Error in get_tweet_data: ' + e)
        return ''






# ----------------------------------------------------------
# Provided Functions: Do Not Change
# ----------------------------------------------------------

def get_twitter_api(consumer_key=consumer_key, consumer_secret=consumer_secret):
    ''' creates an Api object using the consumer_key and consumer_secret
        defined above
    '''
    try:
        return twitter.Api(consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           application_only_auth=True,
                           sleep_on_rate_limit=True)
    except twitter.error.TwitterError as e:
        print('Error in get_api: ' + e)
        return False

def test_twitter_connection(consumer_key=consumer_key,
                            consumer_secret=consumer_secret,
                            screen_name=test_screen_name ):
    ''' simple test to verify program is connected to twitter properly '''
    try:
        api = get_twitter_api()    
        timeline = api.GetUserTimeline(screen_name=screen_name)
        most_recent_tweet = timeline[0]
        print(most_recent_tweet.text)
    except twitter.error.TwitterError as e:
        print('Error in test_connection: ' + e)
        return False


def get_gmaps_client(geocode_api_key=geocode_api_key):
    ''' get google maps client with given api key '''
    return googlemaps.Client(key=geocode_api_key)

def test_gmaps_connection(geocode_api_key=geocode_api_key,
                          address=test_address):
    ''' test connection to google maps library '''
    gmaps_client = googlemaps.Client(key=geocode_api_key)
    geocode_result = gmaps_client.geocode(address)
    print_result(geocode_result)

def print_result(result):
    '''print each dictionary in the result list returned from gmaps '''
    for D in result:
        print_dict(D, 0)

def print_dict(D, tabs):
    '''print items in a dictionary indented with dotted lines between'''
    indent = '    ' * tabs
    for k,v in D.items():
        if tabs == 0:
            print('----------------------------------')
        if type(v) == dict:
            print(indent + str(k) + ': ')
            print_dict(v, tabs+1)
        elif type(v) == list:
            print(indent + str(k) + ': ')
            print_list(v, tabs+1)
        else:
            print(indent + str(k) + ' = ' + str(v))
    if tabs == 0:
        print('----------------------------------')
            
def print_list(L, tabs):
    '''print items in a list indented with dotted lines between'''
    indent = '    ' * tabs
    for i in range(len(L)):
        if type(L[i]) == list:
            print_list(L[i], tabs+1)
        elif type(L[i]) == dict:
            print_dict(L[i], tabs)
        else:
            print(indent + str(L[i]))
        if i < len(L)-1:
            print(indent + '..............' + '....' * (5 - tabs))


main()



###TEST CASES FOR SEARCH:
##	How would you like to search twitter?
##1. By username
##2. By keywords
##3. By location
##4. Exit
##3
##
##You can find trending tweets near a place. Where do you want to see trending tweets?
##Colgate University
##
##Sent near Colgate University:
##Tweet from @DmmK59 at 10:46 AM on Thu 14, 2017: "@DRFLivingston @StonestreetFarm Magnificent!!!!"
##Tweet from @MaryWilsonNews at 10:46 AM on Thu 14, 2017: "Search for missing Schoharie County hunter continues at 8am - here’s where the 77 year old’s truck was found yester… https://t.co/6avXgKjr7Y"
##
##	How would you like to search twitter?
##1. By username
##2. By keywords
##3. By location
##4. Exit
##1
##	Search by username
##
##1. Get information about a user
##2. Get tweets by a user
##3. Quit
##1
##What is the username? colgateuniv
##@colgateuniv (Colgate University) "Established 1819."
##
##1. Get information about a user
##2. Get tweets by a user
##3. Quit
##2
##What is the username? colgateuniv
##Tweet from @colgateuniv at 01:35 AM on Thu 14, 2017: "RT @Meeannimal: Karaoke at @colgateuniv #AOC Holiday Mixer? Best. Alumni. Group. Ever. #AlumniofColor"
##Tweet from @colgateuniv at 01:13 AM on Thu 14, 2017: "Professor Andy Pattison on research and teaching climate change, filmed on the Darwin Thinking Path in the fall https://t.co/vbQtekhODV"
##Tweet from @colgateuniv at 11:25 PM on Wed 13, 2017: "RT @LOHADdotcom: Legendary Concerts and Performances at Colgate University https://t.co/vCQf8whz9Y"
##Tweet from @colgateuniv at 09:13 PM on Wed 13, 2017: "Happy 13th.   Happy last day of classes."
##Tweet from @colgateuniv at 08:20 PM on Wed 13, 2017: "RT @SenatorFunke: Our Business of the Month for December is Christy's Cafe in Victor.  Owner Christy Mills, a recent graduate of Colgate Un…"
##Tweet from @colgateuniv at 07:13 PM on Wed 13, 2017: "Biology Fall Poster Session https://t.co/Ipdjb20jhK https://t.co/ymQzjSrajo"
##Tweet from @colgateuniv at 06:13 PM on Wed 13, 2017: "Dean Gary Ross ‘77 moderates a panel to answer your admission questions.   Find direct links to the questions in th… https://t.co/0rhHR0AR4b"
##Tweet from @colgateuniv at 04:13 PM on Wed 13, 2017: "Geochemist Richard April is quoted in this @sciencemagazine piece about the possible role air pollution played in a… https://t.co/otqBj22QAw"
##Tweet from @colgateuniv at 03:53 PM on Wed 13, 2017: "RT @katiegrandis: Fond memories receiving mine...almost EIGHT years ago. Congratulations, Class of 2022! @colgateuniv https://t.co/oHyffKmG…"
##Tweet from @colgateuniv at 03:13 PM on Wed 13, 2017: "Today we send out the admittance notices to people who applied early decision for the Class of 2022.   Welcome to C… https://t.co/vokzfz0EPk"
##Tweet from @colgateuniv at 01:33 PM on Wed 13, 2017: "RT @megannleo: God bless the @colgateuniv librarian going around every floor at 4 a.m. to give chocolate to the students still desperately…"
##Tweet from @colgateuniv at 01:13 PM on Wed 13, 2017: "Happy 13th  https://t.co/dRX6wvXiFT"
##Tweet from @colgateuniv at 02:13 AM on Wed 13, 2017: "Benton Hall https://t.co/oVw7kZAUOV"
##Tweet from @colgateuniv at 12:13 AM on Wed 13, 2017: "Professor Rebecca Shiner was interviewed for this article on the hopeful science of personality change https://t.co/SzWpZsAIYF"
##Tweet from @colgateuniv at 11:13 PM on Tue 12, 2017: "Alternative Cinema: Student Showcase https://t.co/BmnpyaoD3j https://t.co/QknzXMwnnN"
##Tweet from @colgateuniv at 10:13 PM on Tue 12, 2017: "Men's basketball (@colgatembb) vs NJIT https://t.co/vBauEKw4RR https://t.co/xEo42kP0FZ"
##Tweet from @colgateuniv at 09:13 PM on Tue 12, 2017: "Health Sciences at Colgate  https://t.co/esPTv2z6li"
##Tweet from @colgateuniv at 08:13 PM on Tue 12, 2017: "#gameday https://t.co/QMJlhRfBwy"
##Tweet from @colgateuniv at 07:45 PM on Tue 12, 2017: "Featuring Jesse Winchester '08 https://t.co/Tm1tksNxpK"
##Tweet from @colgateuniv at 07:42 PM on Tue 12, 2017: "RT @ColgateFB: Congratulations Grant Breneman on finishing top 10 in voting for the @FCS_STATS Jerry Rice Award as national freshman of the…"
##
##1. Get information about a user
##2. Get tweets by a user
##3. Quit
##3
##
##	How would you like to search twitter?
##1. By username
##2. By keywords
##3. By location
##4. Exit
##2
##Input your keyword(s): melee
##
##tweets containing "melee":
##Tweet from @AdamSchefter at 09:13 PM on Mon 11, 2017: "No Seahawks players will be suspended for Sunday's actions against Jacksonville, though NFL still reviewing melee u… https://t.co/czlqQJh5k1"
##Tweet from @City_Watch at 10:47 PM on Sun 10, 2017: "Mourinho allegedly had water squirted at him and was hit on the head by an empty plastic bottle while a melee ensue… https://t.co/OedpPZBOsM"
##Tweet from @BigHamm3r at 10:48 AM on Thu 14, 2017: "Misaki's limitations were always that her high damage potential was restricted by her melee range and her need for… https://t.co/YxpCzDBUmT"
##Tweet from @genjitxt at 10:38 AM on Thu 14, 2017: "Buff me to include a melee move that allows me to kill everyone in sight, and remain invulnerable, and perform team… https://t.co/NnydzgrjP6"
##Tweet from @NEG_ssbm at 10:35 AM on Thu 14, 2017: "@Sigh_melee Sighさん 名古屋オフで会えるの楽しみにしてる"
##
##	How would you like to search twitter?
##1. By username
##2. By keywords
##3. By location
##4. Exit
##4






