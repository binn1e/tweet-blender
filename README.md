#tweet-blender

A Python script that : 

1. Reports basics and funny stats about your Twitter usage  
2. Allows you to sort and export your tweets using advanced content filtering

##usage :

As soon as you get it from twitter.com, just unzip your twitter archive on your hard drive and save the **common_words.txt_ file**, **common_domains.txt** file, and **tweet_blender.py** script at the root of the archive folder to run it.  

### stats feature : 

<code>$ python tweet_blender.py</code>  
Runs the script to reports and print stats stdout.  

The stats feature displays many tops 5 which look like this (most common uncommon words tweeted) :  
<pre>
× stop repeating yourself :
— 1.  fucking
— 2.  fuck
— 3.  code
— 4.  super
— 5.  cool
</pre>  

If you want to resize tops, please use <code>-t</code> option like this :  

<code>$ python tweet_blender.py -t 42</code> - whenever possible, this displays your 42 most tweeted smileys, internet domains, etc...

FYI : data used in previous example is courtesy of my boyfriend, and yes, in case you're wondering : I am very proud.  

### sort and export feature :  

All of the commands listed below will export selected tweets to the **sorted.csv** file.  

<code>$ python tweet_blender.py -aany pattern [pattern ...]</code>  
Adds to selection tweets containing pattern or pattern n. Patterns maybe a word, "an expression" or "a regexp?". 

<code>$ python tweet_blender.py -aall pattern [pattern ...]</code>  
Adds to selection tweets containing pattern and pattern n.  

<code>$ python tweet_blender.py -rany pattern [pattern ...]</code>  
Remove from selection tweets containing pattern or pattern n.  

<code>$ python tweet_blender.py -rall pattern [pattern ...]</code>  
Remove from selection tweets containing pattern and pattern n.  

Both <code>[-aany]</code> or <code>[-aall]</code> inculsion options can be combined with <code>[-rany]</code> or <code>[-rall]</code> exclusion options.  
For example :  

<code>$ python tweet_blender.py -aany pizza "video games" -rall programming coffee</code>  
Adds to selection tweets that contain 'pizza' or 'video games' and remove from selection tweets that contain both 'programming' and 'coffee'.  

<code>$ python tweet_blender.py -aall @binnie 'cof+e+' -rany pizza donut cookie</code>  
Adds to selection tweets that contain '@binnie' and match 'cof+e+' and remove from selection tweets that contain 'pizza' or 'donut' or 'cookie'.  

To make your query case insensitive, add <code>[-i]</code> option   

## help:

<pre><code>$ python tweet_blender.py -h   
usage: tweet_blender [-h] [-aany pattern [pattern ...] | -aall pattern
                     [pattern ...]] [-rany pattern [pattern ...] | -rall
                     pattern [pattern ...]] [-i] [-t size]

Process some tweets.

optional arguments:
  -h, --help            show this help message and exit
  -aany pattern [pattern ...]
                        Adds to selection each tweet containing any of the
                        listed expressions.
  -aall pattern [pattern ...]
                        Adds to selection each tweet containing all of the
                        listed expressions.
  -rany pattern [pattern ...]
                        Remove from selection each tweet containing any of the
                        listed expressions.
  -rall pattern [pattern ...]
                        Remove from selection each tweet containing all of the
                        listed expressions.
  -i                    Make command case insensitive.
  -t size               Define tops size.
</code></pre>
## notes:

- Please feel free to edit the **common_words.txt** file or **common_domains.txt** file as you wish in order to obtain more accurate personal and funny results.  
- **common_words.txt** contains around 1000 french words so you may want to delete them if you tweet only in english, so the script can run quicker.  

Dependencies : none.
