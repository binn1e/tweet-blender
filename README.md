tweet-blender
=============

A Python script that : 

1. Reports bascis and funny stats about your Twitter usage  
2. Allows you to sort and export your tweets using advanced content filtering

usage :
-------
- As soon as you get it from twitter.com, just unzip your twitter archive on your hard drive and save the **common_words.txt_ file**, **common_domains.txt** file, and **tweet_blender.py** script at the root of the archive folder to run it.  

<code>$ python tweet_blender.py</code>  
Runs the script to reports and print stats stdout.  

<code>$ python tweet_blender.py -iany pattern [pattern ...]</code>  
Exports tweets containing pattern or pattern n. patterns maybe a word, "an expression" or "a regexp?"  

<code>$ python tweet_blender.py -iall pattern [pattern ...]</code>  
Exports tweets containing pattern and pattern n.  

<code>$ python tweet_blender.py -eany pattern [pattern ...]</code>  
Exports tweets not containing pattern or pattern n.  

<code>$ python tweet_blender.py -eall pattern [pattern ...]</code>  
Exports tweets not containing pattern and pattern n.  

Both <code>[-iany]</code> or <code>[-iall]</code> inculsion options can be combined with <code>[-eany]</code> or <code>[-eall]</code> exclusion options.  
For example :  

<code>$ python tweet_blender.py -iany pizza "video games" -eall programming coffee</code>  
Exports tweets that contain 'pizza' or 'video games' but don't contain both 'programming' and 'coffee'.  

<code>$ python tweet_blender.py -iall @binnie 'coffee' -eany pizza donut cookie</code>  
Exports tweets that contain '@binnie' and 'coffee' but don't contain 'pizza' or 'donut' or 'cookie'.  

help:
-----

<pre><code>$ python tweet_blender.py -h   
usage: tweet_blender [-h] [-iany pattern [pattern ...] | -iall pattern  
                     [pattern ...]] [-eany pattern [pattern ...] | -eall      
                     pattern [pattern ...]]
                     
Process some tweets. 

optional arguments:      
  -h, --help            show this help message and exit  
  -iany pattern [pattern ...]  
                        Each exported tweet will contain any listed expressions.  
  -iall pattern [pattern ...]  
                        Each exported tweet will contain all listed expressions.  
  -eany pattern [pattern ...]  
                        Each exported tweet won't contain any listed expressions.  
  -eall pattern [pattern ...]  
                        Each exported tweet won't contain all listed expressions.  
</code></pre>
notes:
------

- Please feel free to edit the **common_words.txt** file or **common_domains.txt** file as you wish in order to obtain more accurate personal and funny results.  
- **common_words.txt** contains around 1000 french words so you may want to delete them if you tweet only in english, so the script can be quicker.  

Dependencies : none.
