StuffDb  -- A database system about lots of different kinds of Stuff

( Also see the Wiki )

A desktop gui system using qt to track all sorts of "stuff"  
As an addition provides for nice workflow tracking, executable code examples
bookmarks and more.

  stuff categories include:
* text notes = help 
* physical item, a collection, a set of woodworking = stuff
* tools... like hammers, cnc mills, computers  = stuff document
* an address book ++   = people document 
* information about kinds of plants = plant document, and for a particular plant in a particurla place a planting document
* pictures with notes ... linked to other documents = picture document
* albums documents: a collection of pictures

* An application superpower:
  ** Notes can includ "hyper commands" that search wiithin the application or execute
     code of various types ( Python, Bash .... SQL ) or can be used as an application
     launcher or a url bookmark.
      ......

Most of the documentation for the system will be in its own database, I will need
to make a version for this repository, right now it is just on my system.  There
is just a bit more in this repos wiki.

This is my first time with qt for sql, it has been an adventure

Status:
  At this point a lot of the Stuffdb works, but still very far from polished system.
  The current db is around the notes/help document which works fairly well.

  Other documents basically work but can be rough.
  
  If you want to try it out: contact me and I will make the repository work ( for you ), right
  now while it works on my desktop the repo is primarly for backup not distribution.

  Will soon have a db for all the documents, mostly empty.
  I am not yet shipping a good starter db but will make one on request.

This is a reimplemtation of a system I wrote 20 years ago in Powerbulider, it
will take a long time to replicat all of its features, but I will be able
to add new many new features, such as geolocation for maps, and builtin
editor for long text.

Note:
  I still like to keep most of the code right in the git root, see main.py to 
  start it up ( some code probably missing from repository, but will come in time )


Install:
  There is none, just download all the files and try to run it in
  some sort of development environment.
  
  When it complains about dependencies add them

  I am running in Linux Mint, Python 13 it is developed/built in AnacondaSpyder

  There is a parameter.py file and a adjust_path.py file that you will probably
  need help in tweaking.  I have had others install this application and get running in about 15 minutes.

Requirements  no .txt file
  Biggest one is probably pyqt5 -- i install by using anaconda and spyder which
    includes it.

  wat inspector -- on github think it is pip install wat-inspector 

  will work on this in a bit feel free to send feedback

  
