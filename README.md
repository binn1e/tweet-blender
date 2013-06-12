tweet-blender
=============

A python script that : 

1] Reports funny stats about your Twiter usage  
2] Allows you to sort and export your tweets using advanced content filtering

usage :
======
- As soon as you get it from twitter.com, just unzip your twitter archive on your hard drive and save the common_words.txt file, common_domains.txt file, and tweet_blender.py script at the root of the archive folder to run it.

$ python tweet_blender.py
Runs the script to reports and print stats stdout.

$ python tweet_blender.py -iany pattern [pattern n]
Exports tweets containing pattern or pattern n. patterns maybe a word, "an expression" or "a regexp?"

$ python tweet_blender.py -iall pattern [pattern n]
Exports tweets containing pattern and pattern n. 

$ python tweet_blender.py -eany pattern [pattern n]
Exports tweets not containing pattern or pattern n.

$ python tweet_blender.py -eall pattern [pattern n]
Exports tweets not containing pattern and pattern n.

Both [-iany] or [-iall] inculsion options can be combined with [-eany] or [-eall] exclusion options. 
For example :

$ python tweet_blender.py -iany pizza "video games" -eall programming coffee
Exports tweets that contain 'pizza' or 'video games' but don't contain both 'programming' and 'coffee'.

$ python tweet_blender.py -iall @binnie 'coffee' -eany pizza donut cookie
Exports tweets that contain '@binnie' and 'coffee' but don't contain 'pizza' or 'donut' or 'cookie'.

help:
=====
$ python tweet_blender.py -h

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

notes:
======

- Please feel free to edit the common_words.txt files or common_domains.txt files as you wish in order to obtain more accurate personal and funny results.

Dependencies : none.
