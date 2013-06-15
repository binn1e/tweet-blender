#!/usr/bin/python
# -*- coding: UTF-8 -*-

""" 
~ 	tweet_blender.py - v1.0
~	Reports basics and funny statistics of your Twitter usage, illustrated by random picked-up examples. 
~ 	Allows you to sort and export tweets using advanced content filtering.
~ 	Run this script against your Twitter archive. 
~ 	Sorry for the nasty comments.
~	Created by Sabrina Matrullo on 2013-06-15
~
"""

import re, csv 

from random import randint
from datetime import datetime
from argparse import ArgumentParser

csv_path = 'tweets.csv'

# useful patterns
classicRT = "RT\s@"
quotedRT = "“@|\"@" 
username = "@\w+"
hashtag = "#\w+"
happySmiley = "[:;=X]'*[)\]D>]+$"
sadSmiley = "[:=]'*[(/[<]+$"
kissSmiley = "[:;=][*Xx]+$"
naughtySmiley = "[:;=X][P3]+$"
happyJapanese = "\(?\^_*\^\)?$" 
sadJapanese =  "\(?T_*T\)?$"
basicWord = "[a-z]{3,}"
picService = "insta|twitpic|imgur|lockerz|tinypic|imageshack|yfrog"
lol = "l+o+l+$|o+l+o+l$"
hilarity = "h+a+h+a+|a+h+a+h+|h+u+h+u+|u+h+u+h+|h+e+h+e+|e+h+e+h+|h+i+h+i+|i+h+i+h+|h+o+h+o+|o+h+o+h+"
aww = "aww+"
url = "(https?://([-\w\.]+)+(:\d+)?(/([\w/_\.]*(\?\S+)?)?)?)"
heart = "&lt;3"
strip = '.,;:()!?"”'

# tweet length segmentation (i splitted 140 in 3 parts of about 46 characters.)
shortRange 	= [0, 46]
midRange 	= [47, 94]
longRange 	= [95, 139]
maxRange 	= [140, 140]

with open("common_words.txt", "r") as ew:
	excluded_words = [word.lower().rstrip() for word in ew]

with open("common_domains.txt", "r") as cd:
	excluded_domains = [domain.lower().rstrip() for domain in cd]

def loadTweets(path):
	tweets = []
	csv_file_object = csv.reader(open(path, 'rb'), delimiter = ',', quotechar = '"') 
	csv_file_object.next()
	for row in csv_file_object: 
		tweets.append(row)
	return tweets

def count(tweets):	
	return len(tweets)

def getTimestamp(tweet):
	return tweet[5][0:19]

def getSource(tweet):
	return tweet[6]

def getTweet(tweet):
	return tweet[7]

def getUrl(tweet):
	if len(tweet) > 8 :
		return tweet[8]
	else: return '' 

def getDomain(url):  
	parts = re.split("\/", url)
	match = re.match("([\w\-]+\.)*([\w\-]+\.\w{2,6}$)", parts[2]) 
	if match != None:
		if re.search("\.uk", parts[2]): 
			match = re.match("([\w?\-?]+\.)*([\w?\-?]+\.[\w?\-?]+\.\w{2,6}$)", parts[2])
		return match.group(2)
	else: return ''

def getData(data, key):	
	for line in data:
		if line[0] == key:
			return line[1]

def getLinkTweets(tweets):
	links = []
	for tweet in tweets:
		if getUrl(tweet) != '':
			links.append(tweet)
	return links

def getPicTweets(tweets):
	pics = []
	for tweet in tweets:
		if re.search(picService, getUrl(tweet)):
			pics.append(tweet)
	return pics

def getTweetsByLength(tweets, lengthRange):
	measuredTweets = []
	for tweet in tweets:
		if len(getTweet(tweet)) >= lengthRange[0] and len(getTweet(tweet)) <= lengthRange[1] :
			measuredTweets.append(tweet)
	return measuredTweets

def searchTweets(tweets, patterns = [], ic = False, reverse = False):
	matchingTweets = []
	for tweet in tweets:
		match = False
		for pattern in patterns:
			if ic:			
				if re.search(pattern, getTweet(tweet), re.IGNORECASE):
					match = True
			else: 
				if re.search(pattern, getTweet(tweet)):
					match = True
		if not reverse and match: matchingTweets.append(tweet)
		if reverse and not match: matchingTweets.append(tweet)
	return matchingTweets

# fetch a random, iedally midlengthy tweet
def pickUpTweet(tweets):
	if len(tweets) == 1: return tweets[0]
	else: 
		selector = getTweetsByLength(tweets, midRange)
		if len(selector) == 0: 
			selector = getTweetsByLength(tweets, shortRange)
			if len(selector) == 0:
				selector = getTweetsByLength(tweets, longRange)		
				if len(selector) == 0:
					selector = getTweetsByLength(tweets, maxRange)	
		return selector[randint(0, len(selector) - 1)]

# a retweet can be pure or commented
def sortRT(tweets): 
	allRT= []
	pureRT= []
	commentedRT= []
	for tweet in tweets:	
		if re.search(classicRT, getTweet(tweet)) or re.search(quotedRT, getTweet(tweet)):
			allRT.append(tweet)
			if re.search(classicRT, getTweet(tweet)): 
				rtParts = re.split(classicRT, getTweet(tweet))			
				if rtParts[0] == '': 
					pureRT.append(tweet)
				else: 
					commentedRT.append(tweet)
			else:
				rtParts = re.split(quotedRT, getTweet(tweet))			
				if rtParts[0] == '': 
					pureRT.append(tweet)
				else: 
					commentedRT.append(tweet)
	return [["all", allRT], ["pure", pureRT], ["commented", commentedRT]]

def sortDomains(tweets):
	domainCount = {}
	for tweet in tweets:
		domain = getDomain(getUrl(tweet))
		if domain not in excluded_domains:
			if domain in domainCount:
				domainCount[domain] += 1
			else:
				domainCount[domain] = 1
	domains = sorted(domainCount, key=domainCount.get, reverse = True)	
	return domains

def sortEntities(tweets, patterns = [], strip = '', exclude = [], lc = False, ic = False):
	entityCount = {}
	for tweet in tweets:
		words = getTweet(tweet).split()
		for word in words:
			match = False
			for pattern in patterns:
				if ic: 
					if re.match(pattern, word, re.IGNORECASE):
						match = True
				else:
					if re.match(pattern, word):
						match = True
			if match:
				if lc: 
					word = word.lower()
				word = word.strip(strip)
				if word not in exclude :				
					if word in entityCount:
						entityCount[word] += 1
					else:
						entityCount[word] = 1
	entities = sorted(entityCount, key=entityCount.get, reverse = True)	
	return entities

def getEntities(tweets, patterns = [], strip = '', ic = False):
	entities = []
	for tweet in tweets:
		words = getTweet(tweet).split()
		for word in words:
			match = False
			for pattern in patterns:
				if ic:
					if re.match(pattern, word, re.IGNORECASE):
						match = True
				else: 
					if re.match(pattern, word):
						match = True
			if match:
				word = word.strip(strip)
				if re.match(pattern, word):
					entities.append(word)
	return entities

def avgLength(words):
	if len(words) > 0:
		charCount = 0
		for word in words:
			charCount += len(word)
		return float(charCount) / float(len(words)) 

def countChars(tweet, rt = False):
	wordCount = 0
	charCount = 0
	if rt :
		if re.search(classicRT, getTweet(tweet)): rtParts = re.split(classicRT, getTweet(tweet))	 
		else: rtParts = re.split(quotedRT, getTweet(tweet))	 
		if not rtParts[0] == '': words = rtParts[0].split()
	else: words = getTweet(tweet).split()
	for word in words: 
		if not re.match(username, word) and not re.match(url, word):  
			wordCount += 1
			charCount += len(word)
	return [wordCount, charCount]

def biblioMetrics(not_rt, com_rt):	
	avgPage = 1650 # average from considering a book page contains between 1500 and 1800 characters and a book 280 pages.
	avgBook = 280  # i feel like shit for calculating this - but some of us probably need it badly.
	totalChar = 0 
	totalWord = 0 
	for tweet in not_rt: 
		chars = countChars(tweet)
		totalWord += chars[0]
		totalChar += chars[1]
	for tweet in com_rt:
		chars = countChars(tweet, True)
		totalWord += chars[0]
		totalChar += chars[1]
	return [["chars", totalChar], ["words", totalWord],["pages", float(totalChar / avgPage)], ["books", float(totalChar / avgPage) / float(avgBook)]]

def numberDisplay(intro, unit, number):
	if number > 0: print '\n\t× %s : %.1f %s.' % (intro, number, unit)	

def topDisplay(top, ranking = True):
	i = 1
	for champion in top:
		if i < 10:
			if ranking: print '  \t— %s.  %s' % (i, champion)
			else: print '  \t— %s' % (champion)
		else:		
			if ranking: print '  \t— %s. %s' % (i, champion)
			else: print '  \t— %s' % (champion)
		i += 1
	return

def topCut(top, limit, randomize = False):
	if not randomize: return top[0:limit]
	else:
		rand = []
		randNumbers = []
		if limit > len(top) - 1: limit = len(top) -1
		while len(randNumbers) < limit:
			number = randint(0, len(top) - 1)
			if number not in randNumbers: randNumbers.append(number)
		for x in randNumbers:
			rand.append(top[x])
		return rand

def statsDisplay(volume_intro, tweets, total_intro = '', total = 0, displayTweet = True, sub = True):	
	volume = count(tweets)	
	if total: prop = float(volume) / float(total) * 100
	if volume != 0:
		if displayTweet:
			tweet = pickUpTweet(tweets)
			text = getTweet(tweet)	
			ts = getTimestamp(tweet)
			day = int(ts[8:10])
			if day > 3: qual = "th"
			elif day == 1: qual = "st"
			else: qual = "rd"
			date = datetime(int(ts[0:4]), int(ts[5:7]), day, int(ts[11:13]), int(ts[14:16]), int(ts[17:19]))
			date = date.strftime("%a %-d" + qual + " %b %Y, %H:%M").lower()
			if sub: 
				text = re.sub('&gt;', '>', text)
				text = re.sub('&lt;', '<', text)
			if total: 
				if len(text) > 94: print '\t× %s :\n\t— %s, %.2f%% of %s\n\t> [%s]\n\t> %s\n' % (volume_intro, volume, prop, total_intro, date, text)
				else: print '\t× %s :\n\t— %s, %.2f%% of %s\n\t> [%s] %s\n' % (volume_intro, volume, prop, total_intro, date, text) 
			else: 
				if len(text) > 94: print '\t× %s :\n\t— %s\n\t> [%s]\n\t> %s\n' % (volume_intro, volume, date, text)
				else : print '\t× %s :\n\t— %s\n\t> [%s] %s\n' % (volume_intro, volume, date, text)
		else:
			if total: print '\t× %s :\n\t— %s, %.2f%% of %s\n' % (volume_intro, volume, prop, total_intro)
			else: print '\t× %s :\n\t— %s\n' % (volume_intro, volume)
	return

def sortTweets(tweets):
	sortedTweets = []
	sortedTweets.append(["raw_tweets", tweets])
	rawTweets = getData(sortedTweets, "raw_tweets")
	sortedTweets.append(["all_pure_output_tweets", searchTweets(searchTweets(tweets, ["^"+username], reverse = True), 
			    [classicRT, quotedRT], reverse = True)])
	pureOutputTweets = getData(sortedTweets, "all_pure_output_tweets")
	sortedTweets.append(["short_pure_output_tweets", getTweetsByLength(pureOutputTweets, shortRange)])
	sortedTweets.append(["mid_pure_output_tweets", getTweetsByLength(pureOutputTweets, midRange)])
	sortedTweets.append(["long_pure_output_tweets", getTweetsByLength(pureOutputTweets, longRange)])
	sortedTweets.append(["max_pure_output_tweets", getTweetsByLength(pureOutputTweets, maxRange)])
	sortedTweets.append(["reply_tweets", searchTweets(tweets, ["^"+username])])
	sortedTweets.append(["mention_tweets", searchTweets(tweets, [username])])
	sortedTweets.append(["all_output_but_replies", searchTweets(tweets, ["^"+username], reverse = True)])
	allOutputButReplies = getData(sortedTweets, "all_output_but_replies")
	RTs = sortRT(allOutputButReplies)
	sortedTweets.append(["pure_rt_tweets", getData(RTs, "pure")])
	sortedTweets.append(["commented_rt_tweets", getData(RTs, "commented")])
	sortedTweets.append(["all_rt_tweets", getData(RTs, "all")])
	sortedTweets.append(["all_output_but_rt" , searchTweets(tweets, [classicRT, quotedRT], reverse = True)])
	allOutputButRT = getData(sortedTweets, "all_output_but_rt")
	linkTweets = getLinkTweets(allOutputButRT)
	sortedTweets.append(["link_tweets", linkTweets])
	sortedTweets.append(["pic_tweets", getPicTweets(linkTweets)])
	sortedTweets.append(["hashtag_tweets", searchTweets(allOutputButRT, ["\s"+hashtag])])
	sortedTweets.append(["sorted_domains", sortDomains(getData(sortedTweets, "link_tweets"))])
	sortedTweets.append(["aww_tweets", searchTweets(allOutputButRT, ["\s"+aww], ic = True)])
	sortedTweets.append(["happy_smiley_tweets", searchTweets(allOutputButRT, ["\s"+happySmiley])])
	sortedTweets.append(["sad_smiley_tweets", searchTweets(allOutputButRT, ["\s"+sadSmiley])])
	sortedTweets.append(["kiss_smiley_tweets", searchTweets(allOutputButRT, ["\s"+kissSmiley])])
	sortedTweets.append(["naughty_smiley_tweets", searchTweets(allOutputButRT, ["\s"+naughtySmiley])])
	sortedTweets.append(["happy_japan_tweets", searchTweets(allOutputButRT, ["\s"+happyJapanese])])
	sortedTweets.append(["sad_japan_tweets", searchTweets(allOutputButRT, ["\s"+sadJapanese])])
	sortedTweets.append(["heart_tweets", searchTweets(allOutputButRT, [heart])])
	sortedTweets.append(["lol_tweets", searchTweets(tweets, ["\s"+lol], ic = True)])
	lolTweets = getData(sortedTweets, "lol_tweets")
	sortedTweets.append(["lulz", getEntities(lolTweets, [lol], strip, True)])
	sortedTweets.append(["avg_lol_length", avgLength(getData(sortedTweets, "lulz"))])
	sortedTweets.append(["sorted_lulz",  sortEntities(getData(sortedTweets, "lol_tweets"), [lol], strip, ic = True)])
	sortedTweets.append(["hilarity_tweets", searchTweets(tweets, [hilarity], ic = True)])
	hilareTweets = getData(sortedTweets, "hilarity_tweets")
	sortedTweets.append(["hilarities", getEntities(hilareTweets, [hilarity], strip, True)])
	sortedTweets.append(["avg_hilarity_length", avgLength(getData(sortedTweets, "hilarities"))])
	sortedTweets.append(["sorted_hilarities", sortEntities(hilareTweets, [hilarity], strip, ic = True)])
	amusedTweets = []
	amusedTweets.extend(lolTweets)
	amusedTweets.extend(hilareTweets)
	sortedTweets.append(["amused_tweets", amusedTweets])
	sortedTweets.append(["amusements", getEntities(amusedTweets, [lol, hilarity], strip, True)])
	sortedTweets.append(["sorted_amusements",  sortEntities(getData(sortedTweets, "amused_tweets"), [lol,hilarity], strip, ic = True)])
	sortedTweets.append(["avg_amusement_length", avgLength(getData(sortedTweets, "amusements"))])
	sortedTweets.append(["sorted_users", sortEntities(getData(sortedTweets, "mention_tweets"), [username], strip)])
	sortedTweets.append(["sorted_words", sortEntities(rawTweets, ["^"+basicWord], strip, excluded_words, lc = True, ic = True)])
	sortedTweets.append(["sorted_smileys",  sortEntities(rawTweets, 
			    [happySmiley, sadSmiley, kissSmiley, naughtySmiley, happyJapanese, sadJapanese])])
	sortedTweets.append(["sorted_hashtags", sortEntities(getData(sortedTweets, "hashtag_tweets"), [hashtag], strip, ic = True)])
	sortedTweets.append(["amused_replies", searchTweets(amusedTweets, ["^"+username])])
	sortedTweets.append(["sorted_entertainers", sortEntities(getData(sortedTweets, "amused_replies"), [username], strip)])
	sortedTweets.append(["bibliometrics", biblioMetrics(allOutputButRT, getData(sortedTweets, "commented_rt_tweets"))])
	return sortedTweets

def displayStats(data, cut):
	totalTweets = count(getData(data, "raw_tweets"))
	totalAllOutputButRT = count(getData(data, "all_output_but_rt"))

	print '\n\t~ about everything ~' 
	print '\t---------------------\n' 
	statsDisplay("raw tweets", getData(data, "raw_tweets"), '', 0, False)
	
	print '\n\t~ pure output tweets [tweets w/o retweets or replies] segmented by length ~' 
	print '\t---------------------------------------------------------------------------\n' 
	statsDisplay("short pure output tweets", getData(data, "short_pure_output_tweets"), "total tweets", totalTweets)
	statsDisplay("mid pure output tweets", getData(data, "mid_pure_output_tweets"), "total tweets", totalTweets)
	statsDisplay("long pure output tweets", getData(data, "long_pure_output_tweets"), "total tweets", totalTweets)
	statsDisplay("max pure output tweets", getData(data, "max_pure_output_tweets"), "total tweets", totalTweets)
	statsDisplay("all pure output together", getData(data, "all_pure_output_tweets"), "total tweets", totalTweets, False)

	print '\n\t~ social miscellaneous facts  ~' 
	print '\t-------------------------------\n' 
	statsDisplay("replies", getData(data, "reply_tweets"), "total tweets", totalTweets)
	statsDisplay("tweets mentionning users", getData(data, "mention_tweets"), "total tweets", totalTweets, False)
	statsDisplay("pure rt", getData(data, "pure_rt_tweets"), "total tweets", totalTweets)
	statsDisplay("commented rt", getData(data, "commented_rt_tweets"), "total tweets", totalTweets)
	statsDisplay("all rt", getData(data, "all_rt_tweets"), "total tweets", totalTweets, False)

	print '\n\t~ content basics ~' 
	print '\t-------------------\n' 
	statsDisplay("hashtag tweets", getData(data, "hashtag_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("link tweets", getData(data, "link_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("pic tweets", getData(data, "pic_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	print '\t× top domains :' 
	topDisplay(topCut(getData(data, "sorted_domains"), cut))

	print '\n\t~ amusement and emotions ~'  
	print '\t--------------------------\n' 

	statsDisplay("heart tweets", getData(data, "heart_tweets"), "total tweets w/o retweets", totalAllOutputButRT, True)
	statsDisplay("awww tweets", getData(data, "aww_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("happy smiley tweets", getData(data, "happy_smiley_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("sad smiley tweets", getData(data, "sad_smiley_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("kiss smiley tweets", getData(data, "kiss_smiley_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("naughty smiley tweets", getData(data, "naughty_smiley_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("happy jsmiley tweets", getData(data, "happy_japan_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("sad jsmiley tweets", getData(data, "sad_japan_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("lol tweets", getData(data, "lol_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	statsDisplay("hilarity tweets", getData(data, "hilarity_tweets"), "total tweets w/o retweets", totalAllOutputButRT)
	if len(getData(data, "sorted_amusements")) > 2:	
		print "\t× you usually express your amusement like this :"
		topDisplay(topCut(getData(data, "sorted_amusements"), cut, True), False)
		if getData(data, "avg_amusement_length") > 4:		
			print '\n\t[ i know it sounds retarded, right ? no need to be ashamed of yourself. ]'
		numberDisplay("average hilarity length", "characters", getData(data, "avg_hilarity_length"))
		numberDisplay("average lol length", "characters", getData(data, "avg_lol_length"))

	print '\n\t~ awful bibliometrics ~'  
	print '\t-----------------------\n' 
	metrics = getData(data, "bibliometrics")
	books = getData(metrics, "books") 
	if books > 1: outro = "well, like " + str(int(books + 0.1)) + " books of shit no one's gonna read ? congratz, you overachiever."
	else: outro = "working much ? don't you have friends to talk to ? " 
	print '\t× not counted in :\n\t- retweeted content (simply retweeted, or retweeted after a comment you made.)\n\t- mentionned usernames\n\t- copy and pasted URLs\n\ti\'m considering a book page contains 1650 char. on average and a book 280 pages.\n'
	print '\t— %s : %s' % ("total chars", getData(metrics, "chars"))
	print '\t— %s : %s' % ("total words", getData(metrics, "words"))
	print '\t— %s : %s' % ("total pages", getData(metrics, "pages"))
	print '\t— %s : %.1f\n\n\t%s\n' % ("books that could have been written", getData(metrics, "books"), "[ " + outro + " ]")
	
	print '\n\t~ top ranked and loved ones ~' 
	print '\t-----------------------------\n' 
	print '\t× why am i not surprised ?' 
	topDisplay(topCut(getData(data, "sorted_users"), cut))
	print '\n\t× stop repeating yourself :'
	topDisplay(topCut(getData(data, "sorted_words"), cut))
	print '\n\t× this is your twitter face :'
	topDisplay(topCut(getData(data, "sorted_smileys"), cut))
	print '\n\t× can\'t do without :'
	topDisplay(topCut(getData(data, "sorted_hashtags"), cut))
	print '\n\t× devoted entertainers :'
	topDisplay(topCut(getData(data, "sorted_entertainers"), cut))
	print '\t'
	return

def selectTweetsAny(tweets, patterns = [], ic = False):
	output = []
	for tweet in tweets:
		for pattern in patterns:
			if ic: match = re.search(pattern, getTweet(tweet), re.IGNORECASE)
			else: match = re.search(pattern, getTweet(tweet))
			if match: output.append(tweet)	
	return output

def selectTweetsAll(tweets, patterns = [], ic = False):
	output = []
	for tweet in tweets:
		for pattern in patterns:
			if ic: match = re.search(pattern, getTweet(tweet), re.IGNORECASE)
			else: match = re.search(pattern, getTweet(tweet))			
			if not match: break
			else:
				if pattern == patterns[len(patterns)-1]:
					output.append(tweet) 
					break 
				else: continue
	return output

def removeTweetsAny(tweets, patterns = [], ic = False):
	deletion = []
	for tweet in tweets:
		for pattern in patterns:
			if ic: match = re.search(pattern, getTweet(tweet), re.IGNORECASE)
			else: match = re.search(pattern, getTweet(tweet))
			if match:
				deletion.append(tweet)
				break
	for deleted in deletion:
		tweets.remove(deleted)
	return tweets
			
def removeTweetsAll(tweets, patterns = [], ic = False):
	deletion = []
	for tweet in tweets:
		for pattern in patterns:
			if ic: match = re.search(pattern, getTweet(tweet), re.IGNORECASE)
			else: match = re.search(pattern, getTweet(tweet))		
			if not match: break
			else: 
				if pattern == patterns[len(patterns)-1]:
					deletion.append(tweet)
				else:continue 
	for deleted in deletion:
		tweets.remove(deleted)
	return tweets

def writeTweets(tweets):
 	if len(tweets) > 0:
		with open('sorted.csv', 'wt') as tweets_csv_file:
			tweetWriter = csv.writer(tweets_csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
			tweetWriter.writerow(['tweet_id'] + ['in_reply_to_status_id'] + ['in_reply_to_user_id'] + ['retweeted_status_id'] + ['retweeted_status_user_id'] + ['timestamp'] + ['source'] + ['text'] + ['expanded_url'])
			for tweet in tweets:
				tweetWriter.writerow([tweet[0]] + [tweet[1]] + [tweet[2]] + [tweet[3]] + [tweet[4]] + [getTimestamp(tweet)] + [getSource(tweet)] + [getTweet(tweet)] + [getUrl(tweet)]) 

if __name__ == '__main__':

	tweets = loadTweets(csv_path)
	parser = ArgumentParser(prog = "tweet_blender", description = "Process some tweets.")
	iGroup = parser.add_mutually_exclusive_group()
	eGroup = parser.add_mutually_exclusive_group()
	iGroup.add_argument('-aany', type = str, nargs='+', metavar = 'pattern', 
			    help = "Adds to selection each tweet containing any of the listed expressions.") 
	iGroup.add_argument('-aall', type = str, nargs='+', metavar = 'pattern', 
			    help = "Adds to selection each tweet containing all of the listed expressions.") 
	eGroup.add_argument('-rany', type = str, nargs='+', metavar = 'pattern', 
		            help = "Remove from selection each tweet containing any of the listed expressions.") 
	eGroup.add_argument('-rall', type = str, nargs='+', metavar = 'pattern', 
			    help = "Remove from selection each tweet containing all of the listed expressions.") 
	parser.add_argument('-i', action = 'store_true', help = "Make command case insensitive.")
	parser.add_argument('-t', type = int, metavar = 'size', default = 5, help = "Define tops size.")
	args = parser.parse_args()
	if args.aany != None or args.aall != None or args.rany != None or args.rall != None:
		if args.aany != None and args.rany == None and args.rall == None : tweets = selectTweetsAny(tweets, args.aany, args.i)
		if args.aany != None and args.rany != None: tweets = removeTweetsAny(selectTweetsAny(tweets, args.aany, args.i), args.rany, args.i)
		if args.aany != None and args.rall != None: tweets = removeTweetsAll(selectTweetsAny(tweets, args.aany, args.i), args.rall, args.i)
		if args.aall != None and args.rany == None and args.rall == None : tweets = selectTweetsAll(tweets, args.aall, args.i)
		if args.aall != None and args.rany != None: tweets = removeTweetsAny(selectTweetsAll(tweets, args.aall, args.i), args.rany, args.i)
		if args.aall != None and args.rall != None: tweets = removeTweetsAll(selectTweetsAll(tweets, args.aall, args.i), args.rall, args.i)
		if args.rany != None and args.aany == None and args.aall == None : tweets = removeTweetsAny(tweets, args.rany, args.i)
		if args.rall != None and args.aany == None and args.aall == None : tweets = removeTweetsAll(tweets, args.rall, args.i)
		if len(tweets) == 0: print "\n\t× sorry : couldn't find any match.\n"
		else:writeTweets(tweets)
	else: displayStats(sortTweets(tweets), args.t)
