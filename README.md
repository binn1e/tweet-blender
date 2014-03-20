#tweet-blender

A Python script that : 

1. Reports basics and funny stats about your Twitter usage over a specifiable period
2. Allows you to sort and export your tweets using date filtering and advanced content filtering 

##usage :

As soon as you get it from twitter.com, just unzip your archive on your hard drive and place **common_words.txt_ file**, **common_domains.txt** file, and **tweet_blender.py** in the same folder.

### stats feature : 

<code>$ python tweet_blender.py</code>  
Runs the script to reports and print stats stdout.  

<code>$ python tweet_blender.py -start 24062012</code>  
Add date filtering to get data covering a specific period of your life. 

<code>$ python tweet_blender.py -end 31122009</code>  
<code>$ python tweet_blender.py -start 01062009 -end 31122009</code>  

The stats feature displays a bucnh of funny stats and a few of your « top things » which look like following (example below lists most common words tweeted) :  
<pre>
× stop repeating yourself :
— 1.  fucking
— 2.  fuck
— 3.  code
— 4.  super
— 5.  cool
</pre>  

If you want to resize tops to get more data, please use <code>-t</code> option like this :  

<code>$ python tweet_blender.py -t 42</code> - whenever possible, this displays your 42 most tweeted smileys, internet domains, etc...

FYI : data used in previous example is courtesy of my boyfriend, and yes, in case you're wondering : I am very proud!  

### sort and export feature :  

All of the commands listed below desactivate stats feature, and turn script into an exporter that writes selected tweets to the **sorted.csv** file.  

<code>$ python tweet_blender.py -start ddmmyyyy</code>  
Include tweets from given date (included.)

<code>$ python tweet_blender.py -end ddmmyyyy</code>  
Include tweets until given date (included.)

<code>$ python tweet_blender.py -aany pattern [pattern ...]</code>  
Include tweets containing pattern or pattern n. Patterns maybe a word, "an expression" or "a regexp?". 

<code>$ python tweet_blender.py -aall pattern [pattern ...]</code>  
Include tweets containing pattern and pattern n.  

<code>$ python tweet_blender.py -rany pattern [pattern ...]</code>  
Include tweets containing pattern or pattern n.  

<code>$ python tweet_blender.py -rall pattern [pattern ...]</code>  
Include tweets containing pattern and pattern n.  

Both <code>[-aany]</code> or <code>[-aall]</code> inculsion options can be combined with <code>[-rany]</code> or <code>[-rall]</code> exclusion options. Date filtering can be combined with any options. 
For example :  

<code>$ python tweet_blender.py -aany pizza "video games" -rall programming coffee</code>  
Adds to selection tweets that contain 'pizza' or 'video games' and remove from selection tweets that contain both 'programming' and 'coffee'.  

<code>$ python tweet_blender.py -aall @binnie 'cof+e+' -rany pizza donut cookie</code>  
Adds to selection tweets that contain '@binnie' and match 'cof+e+' and remove from selection tweets that contain 'pizza' or 'donut' or 'cookie'.  

To make your query case insensitive, add <code>[-i]</code> option   

<code>$ python tweet_blender.py -start 20122012 -end 27122012 -aany "hip hop" party -rany "oh oh oh" -i</code>

This outputs all your xmas 2012 tweets speaking about hip hop or parties, removing santa jokes.

## help:

<pre><code>
python tweet_blender.py -h
usage: tweet_blender [-h] [-aany pattern [pattern ...] | -aall pattern
                     [pattern ...]] [-rany pattern [pattern ...] | -rall
                     pattern [pattern ...]] [-start pattern [pattern ...]]
                     [-end pattern [pattern ...]] [-i] [-t size]

Process some tweets.

optional arguments:
  -h, --help            show this help message and exit
  -aany pattern [pattern ...]
                        Include tweets containing any of the listed
                        expressions.
  -aall pattern [pattern ...]
                        Include tweets containing all of the listed
                        expressions.
  -rany pattern [pattern ...]
                        Remove tweets containing any of the listed
                        expressions.
  -rall pattern [pattern ...]
                        Remove tweets containing all of the listed
                        expressions.
  -start pattern [pattern ...]
                        Include tweets from given date. [Format : ddmmyyyy]
  -end pattern [pattern ...]
                        Include tweets until given date. [Format : ddmmyyyy]
  -i                    Make command case insensitive.
  -t size               Define tops size.
</code></pre>
## notes:

- Please feel free to edit the **common_words.txt** file or **common_domains.txt** file as you wish in order to obtain more accurate personal and funny results.  
- **common_words.txt** contains around 1000 french words so you may want to delete them if you tweet only in english, so the script can run quicker.  

Dependencies : none.
