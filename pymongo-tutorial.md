I use [mongoDB](http://www.mongodb.org/) along with [Pymongo](http://api.mongodb.org/python/current/) for personal projects only (I hope this changes in the near future though) and not very often to be honest. So this post is more of a quick reference for myself and I hope you guys finds it useful too. I am also writing this post in [Ipython](http://ipython.org/) which I will convert to [markdown](http://en.wikipedia.org/wiki/Markdown) using [nbconvert utility](http://blog.fperez.org/2012/09/blogging-with-ipython-notebook.html) and then push it to my github blog using [Jekyll](http://jekyllbootstrap.com/). Fingers crossed it won't be too difficult.

For this tutorial I'll be using real data from Twitter using the [Tweepy](https://github.com/tweepy/tweepy) package.

Before we start let's see what Wikipedia has to say about MongoDB:

> "MongoDB (from "humongous") is an open source document-oriented database system developed and supported by 10gen. It is part of the NoSQL family of database systems. Instead of storing data in tables as is done in a "classical" relational database, MongoDB stores structured data as JSON-like documents with dynamic schemas (MongoDB calls the format BSON), making the integration of data in certain types of applications easier and faster.

>10gen began Development of MongoDB in October 2007. The database is used by MTV Networks, Craigslist, Foursquare and UIDAI Aadhaar. MongoDB is the most popular NoSQL database management system."

Done - let's start!

## Downloading & Installing MongoDB binaries

1. Head to the MongoDB download page [http://www.mongodb.org/downloads](http://www.mongodb.org/downloads) and get version 2.2.2 (or latest stable version) for your OS (*by the way I'm using OSX for this tutorial so \*nix guys should have no difficulty following along but Windows users may need to change some bits - sorry!*).

2. Unzip mongodb-osx-x86_64-2.2.2.tgz and rename folder mongodb-osx-x86_64-2.2.2 to simply mongodb. I normally move this folder to my personal project folder so feel free to move it in wherever you like. Your mongodb folder should have the following structure: 
`
altons@asgard:~/projects$ls -R mongodb
GNU-AGPL-3.0        README              THIRD-PARTY-NOTICES bin
mongodb/bin:
bsondump     mongod       mongoexport  mongoimport  mongoperf    mongos       mongostat
mongo        mongodump    mongofiles   mongooplog   mongorestore mongosniff   mongotop
altons@asgard:~/projects$
`
3. Kick off the mongodb server:
`
altons@asgard:~/projects$ cd mongodb
altons@asgard:~/projects/mongodb$./bin/mongod --dbpath . --nojournal &
`
4. Open another terminal windows and type: `altons@asgard:~/projects/mongodb$./bin/mongo`

if you something like:
`
MongoDB shell version: 2.2.2
connecting to: test
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
	http://docs.mongodb.org/
Questions? Try the support group
	http://groups.google.com/group/mongodb-user
> 
`
then you are good to go! Type **exit** to quit and go to the previous terminal windows and hit Ctrl+C to kill the server  - we need a bit of customization first.

**Note**: Sometimes (with God as my witness!) Ctrl-C doesn't kill the server and I have to do a `kill -9` on the pid where mongod still running. If that happens - you also need to remove mongodb.lock from your **dbpath** manually otherwise mongoDB will complain next time you fire it up.

## The config file

The option --dbpath . will save your data inside the mongodb folder - I am not a huge fan of this option. I like to keep my data separated from db binaries. So instead I'll use a config file to tell mongoDB where to store my data.

Here it is my config file:
`
# Mongo Production server configuration
# Author: Alberto Negron
# created on: 26/07/2012

dbpath=/Users/altons/projects/data/mongodb/                         # location where I want to store my databases - Use full path
port = 27017                                                        # default port
bind_ip = 127.0.0.1                                                 # default ip
logpath = /Users/altons/projects/data/mongodb/log/mongodb.log       # location where I want to store logs - Use full path
logappend = true                                                    # everytime I fire up mongodb the new log will be appended to a master log file
rest=true                                                           # this option let you check server status at http:\\127.0.0.1:27017
directoryperdb = true                                               # Set to true to modify the storage pattern of the data directory to store each database’s
                                                                    # files in a distinct folder. This option will create directories within the dbpath 
                                                                    # named for each directory

`
and I have saved it as mongo.conf in side the data folder ` (~/projects/data) `.

Now go back to the mongodb folder and use the following command to fire up the server:

`
altons@asgard:~/projects/mongodb$./bin/mongod --config=/Users/altons/projects/data/mongo.conf  --nojournal &
`

Since the option rest is set to true you can check mongodb status via [http://127.0.0.1:28017/](http://127.0.0.1:28017/)

You can have  multiple config files (Prod/Dev/Test) or any combination of servers running on different ports. Options are endless.

## Pymongo

PyMongo is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python. You can install mongodb from either pip or easy_install.

### Connecting to MongoDB

In Pymongo 2.4.1 the connection method has been deprecated. Now we most use MongoClient

<div class="highlight"><pre><span class="kn">import</span> <span class="nn">pymongo</span>

<span class="c"># Connection to Mongo DB</span>
<span class="k">try</span><span class="p">:</span>
    <span class="n">conn</span><span class="o">=</span><span class="n">pymongo</span><span class="o">.</span><span class="n">MongoClient</span><span class="p">()</span>
    <span class="k">print</span> <span class="s">&quot;Connected successfully!!!&quot;</span>
<span class="k">except</span> <span class="n">pymongo</span><span class="o">.</span><span class="n">errors</span><span class="o">.</span><span class="n">ConnectionFailure</span><span class="p">,</span> <span class="n">e</span><span class="p">:</span>
   <span class="k">print</span> <span class="s">&quot;Could not connect to MongoDB: </span><span class="si">%s</span><span class="s">&quot;</span> <span class="o">%</span> <span class="n">e</span> 
<span class="n">conn</span>
</pre></div>


    Connected successfully!!!

<pre>
    MongoClient('localhost', 27017)
</pre>


We are now connected to our server.

### Databases

Mongodb creates databases and collections automatically for you if they don't exist already. A single instance of MongoDB can support multiple independent databases. When working with PyMongo you access databases using attribute style access:

<div class="highlight"><pre><span class="n">db</span> <span class="o">=</span> <span class="n">conn</span><span class="o">.</span><span class="n">mydb</span>
<span class="n">db</span>
</pre></div>


<pre>
    Database(MongoClient('localhost', 27017), u'mydb')
</pre>


If your database name is such that using attribute style access won’t work (like db-name), you can use dictionary style access instead:

<div class="highlight"><pre><span class="n">db</span> <span class="o">=</span> <span class="n">conn</span><span class="p">[</span><span class="s">&#39;sandpit-test&#39;</span><span class="p">]</span>
<span class="n">db</span>
</pre></div>


<pre>
    Database(MongoClient('localhost', 27017), u'sandpit-test')
</pre>


If you need to know what databases are available:

<div class="highlight"><pre><span class="n">conn</span><span class="o">.</span><span class="n">database_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'local']
</pre>


We already created 2 new databases. Why didn't show up with the above command? Well, databases with no collections or with empty collections will not show up with database_names(). Same goes when we try to list empty collections in a database.

We'll test it again once we have populate some collections.

### Collections

A collection is a group of documents stored in MongoDB, and can be thought of as roughly the equivalent of a table in a relational database. Getting a collection in PyMongo works the same as getting a database:

<div class="highlight"><pre><span class="n">collection</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">my_collection</span>
<span class="n">collection</span>
</pre></div>


<pre>
    Collection(Database(MongoClient('localhost', 27017), u'sandpit-test'), u'my_collection')
</pre>


<div class="highlight"><pre><span class="n">db</span><span class="o">.</span><span class="n">collection_names</span><span class="p">()</span>
</pre></div>


<pre>
    []
</pre>


However one must be careful when trying to get existing collections. For example, if you a collection db.user and you type db.usr this is clearly a typo. Unlike an RDBMS, MongoDB won't protect you from this class of mistake.


### Documents

MongoDB stores structured data as JSON-like documents, using dynamic schemas (called BSON), rather than predefined schemas. An element of data is called a document, and documents are stored in collections. One collection may have any number of documents.

Compared to relational databases, we could say collections are like tables, and documents are like records. But there is one big difference: every record in a table has the same fields (with, usually, differing values) in the same order, while each document in a collection can have completely different fields from the other documents. 

All you really need to know when you're using Python, however, is that documents are Python dictionaries that can have strings as keys and can contain various primitive types (int, float,unicode, datetime) as well as other documents (Python dicts) and arrays (Python lists).

To insert some data into MongoDB, all we need to do is create a dict and call .insert() on the collection object:



<div class="highlight"><pre><span class="n">doc</span> <span class="o">=</span> <span class="p">{</span><span class="s">&quot;name&quot;</span><span class="p">:</span><span class="s">&quot;Alberto&quot;</span><span class="p">,</span><span class="s">&quot;surname&quot;</span><span class="p">:</span><span class="s">&quot;Negron&quot;</span><span class="p">,</span><span class="s">&quot;twitter&quot;</span><span class="p">:</span><span class="s">&quot;@Altons&quot;</span><span class="p">}</span>
</pre></div>



Now we need to insert the above document into a collection:

<div class="highlight"><pre><span class="n">collection</span><span class="o">.</span><span class="n">insert</span><span class="p">(</span><span class="n">doc</span><span class="p">)</span>
</pre></div>


<pre>
    ObjectId('50f89eb16577e466cf550b33')
</pre>


Congratulations you have created your first document!!

<div class="highlight"><pre><span class="n">conn</span><span class="o">.</span><span class="n">database_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'sandpit-test', u'local']
</pre>


<div class="highlight"><pre><span class="n">db</span><span class="o">.</span><span class="n">collection_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'system.indexes', u'my_collection']
</pre>


 Now database_names() and collection_names() show database **sandpit-test** and collection **my_collection**.

To recap, we have **databases** containing **collections**. A **collection** is made up of **documents**. Each document is made up of **fields**.


## Tweepy

Before continue with the tutorial, let's get some real data from twitter and insert it in a new database - it'll be definitely more interesting!!!

Let's pull the first 10 result pages with the keyword 'BigData'

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">tweepy</span> <span class="kn">import</span> <span class="n">API</span>
</pre></div>



<div class="highlight"><pre><span class="n">lookup</span> <span class="o">=</span><span class="s">&#39;BigData&#39;</span>
<span class="n">api</span> <span class="o">=</span> <span class="n">API</span><span class="p">()</span>

<span class="n">search</span> <span class="o">=</span> <span class="p">[]</span>
<span class="n">page</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">maxPage</span> <span class="o">=</span> <span class="mi">10</span>
<span class="k">while</span><span class="p">(</span><span class="n">page</span><span class="o">&lt;=</span><span class="n">maxPage</span><span class="p">):</span>
    <span class="n">tweets</span> <span class="o">=</span> <span class="n">api</span><span class="o">.</span><span class="n">search</span><span class="p">(</span><span class="n">lookup</span><span class="p">,</span><span class="n">page</span> <span class="o">=</span> <span class="n">page</span><span class="p">)</span>
    <span class="k">for</span> <span class="n">tweet</span> <span class="ow">in</span> <span class="n">tweets</span><span class="p">:</span>
        <span class="n">search</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">tweet</span><span class="p">)</span>
    <span class="n">page</span> <span class="o">=</span> <span class="n">page</span> <span class="o">+</span> <span class="mi">1</span>
</pre></div>



Let's how many tweets we got from the above search:

<div class="highlight"><pre><span class="nb">len</span><span class="p">(</span><span class="n">search</span><span class="p">)</span>
</pre></div>


<pre>
    149
</pre>


Not bad, let inspect the structure of the first object:

<div class="highlight"><pre><span class="nb">dir</span><span class="p">(</span><span class="n">search</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
</pre></div>


<pre>
    ['__class__',
     '__delattr__',
     '__dict__',
     '__doc__',
     '__format__',
     '__getattribute__',
     '__getstate__',
     '__hash__',
     '__init__',
     '__module__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     '__weakref__',
     '_api',
     'created_at',
     'from_user',
     'from_user_id',
     'from_user_id_str',
     'from_user_name',
     'geo',
     'id',
     'id_str',
     'iso_language_code',
     'metadata',
     'parse',
     'parse_list',
     'profile_image_url',
     'profile_image_url_https',
     'source',
     'text',
     'to_user',
     'to_user_id',
     'to_user_id_str',
     'to_user_name']
</pre>


There is a lot of information that we really don't need. Let's keep only the data related to the tweet and insert it into MongoDB

<div class="highlight"><pre><span class="c"># Define my mongoDB database</span>
<span class="n">db</span> <span class="o">=</span> <span class="n">conn</span><span class="o">.</span><span class="n">twitter_results</span>
<span class="c"># Define my collection where I&#39;ll insert my search</span>
<span class="n">posts</span> <span class="o">=</span> <span class="n">db</span><span class="o">.</span><span class="n">posts</span>
</pre></div>



<div class="highlight"><pre><span class="c"># loop through search and insert dictionary into mongoDB</span>
<span class="k">for</span> <span class="n">tweet</span> <span class="ow">in</span> <span class="n">search</span><span class="p">:</span>
    <span class="c"># Empty dictionary for storing tweet related data</span>
    <span class="n">data</span> <span class="o">=</span><span class="p">{}</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;created_at&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">created_at</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;from_user&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">from_user</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;from_user_id&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">from_user_id</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;from_user_id_str&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">from_user_id_str</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;from_user_name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">from_user_name</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;geo&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">geo</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;id&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">id</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;iso_language_code&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">iso_language_code</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;source&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">source</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;text&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">text</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;to_user&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">to_user</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;to_user_id&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">to_user_id</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;to_user_id_str&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">to_user_id_str</span>
    <span class="n">data</span><span class="p">[</span><span class="s">&#39;to_user_name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tweet</span><span class="o">.</span><span class="n">to_user_name</span>
    <span class="c"># Insert process</span>
    <span class="n">posts</span><span class="o">.</span><span class="n">insert</span><span class="p">(</span><span class="n">data</span><span class="p">)</span>
    
</pre></div>



Dead easy! we have created our collection of tweets, no need to define table and columns beforehand - that's the beauty of MongoDB.

Here it is the structure of the last document inserted:

<div class="highlight"><pre><span class="n">data</span> 
</pre></div>


<pre>
    {'_id': ObjectId('50f99bf66577e466cf550bc8'),
     'created_at': datetime.datetime(2013, 1, 18, 18, 1, 38),
     'from_user': u'Adriana_iSchool',
     'from_user_id': 303810955,
     'from_user_id_str': u'303810955',
     'from_user_name': u'Adriana Rossini',
     'geo': None,
     'id': 292330927105916928L,
     'iso_language_code': u'en',
     'source': u'Twuffer',
     'text': u'New big data firm to pioneer topological data analysis http://t.co/uEHYdcnM via @guardian #BigData #topology',
     'to_user': None,
     'to_user_id': 0,
     'to_user_id_str': u'0',
     'to_user_name': None}
</pre>


#### The _id field


In MongoDB, documents stored in a collection require a unique _id field that acts as a primary key. Because ObjectIds are small, most likely unique, and fast to generate, MongoDB uses ObjectIds as the default value for the _id field if the _id field is not specified; i.e., the mongod adds the _id field and generates a unique ObjectId to assign as its value

## Reading Documents in a Collection

The first and foremost important operation we need to learn is how to retrieve our data from MongoDB. For this, Collections provide the find_one() and find() methods:

- The find_one() method selects and returns a single document from a collection and returns that document (or None if there are no matches). It is useful when you know there is only one matching document, or are only interested in the first match:

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">()</span>
</pre></div>


<pre>
    {u'_id': ObjectId('50f99bf66577e466cf550b34'),
     u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1),
     u'from_user': u'BITechWatch',
     u'from_user_id': 22631958,
     u'from_user_id_str': u'22631958',
     u'from_user_name': u'Marly Cho',
     u'geo': None,
     u'id': 292341338840653825L,
     u'iso_language_code': u'en',
     u'source': u'twitterfeed',
     u'text': u"Everything you ever wanted to know about R functions: It's hard to overstate the importance of function... http://t.co/sD5bG4yg #bigdata",
     u'to_user': None,
     u'to_user_id': 0,
     u'to_user_id_str': u'0',
     u'to_user_name': None}
</pre>


- To get more than a single document as the result of a query we use the find() method. find() returns a Cursor instance, which allows us to iterate over all matching documents. 

posts.find()

For example, we can iterate over the first 2 documents (there are a lot in the collection and this is just an example) in the posts collection:

<div class="highlight"><pre><span class="k">for</span> <span class="n">d</span> <span class="ow">in</span> <span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">()[:</span><span class="mi">2</span><span class="p">]:</span>
    <span class="k">print</span> <span class="n">d</span>
    
</pre></div>


    {u'iso_language_code': u'en', u'to_user_name': None, u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1), u'text': u"Everything you ever wanted to know about R functions: It's hard to overstate the importance of function... http://t.co/sD5bG4yg #bigdata", u'from_user_id_str': u'22631958', u'to_user_id_str': u'0', u'to_user': None, u'source': u'twitterfeed', u'to_user_id': 0, u'from_user': u'BITechWatch', u'id': 292341338840653825L, u'from_user_id': 22631958, u'_id': ObjectId('50f99bf66577e466cf550b34'), u'geo': None, u'from_user_name': u'Marly Cho'}
    {u'iso_language_code': u'en', u'to_user_name': None, u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1), u'text': u'RT @IBMcloud: Big data in the #cloud? Governing a sprawling business resource http://t.co/FDsoNfrf via @jameskobielus #bigdata', u'from_user_id_str': u'115674359', u'to_user_id_str': u'0', u'to_user': None, u'source': u'web', u'to_user_id': 0, u'from_user': u'ibmmb', u'id': 292341338798690304L, u'from_user_id': 115674359, u'_id': ObjectId('50f99bf66577e466cf550b35'), u'geo': None, u'from_user_name': u'Maarten Boerma'}


you can also use the standard python list():

<div class="highlight"><pre><span class="nb">list</span><span class="p">(</span><span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">())[:</span><span class="mi">2</span><span class="p">]</span>
</pre></div>


<pre>
    [{u'_id': ObjectId('50f99bf66577e466cf550b34'),
      u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1),
      u'from_user': u'BITechWatch',
      u'from_user_id': 22631958,
      u'from_user_id_str': u'22631958',
      u'from_user_name': u'Marly Cho',
      u'geo': None,
      u'id': 292341338840653825L,
      u'iso_language_code': u'en',
      u'source': u'twitterfeed',
      u'text': u"Everything you ever wanted to know about R functions: It's hard to overstate the importance of function... http://t.co/sD5bG4yg #bigdata",
      u'to_user': None,
      u'to_user_id': 0,
      u'to_user_id_str': u'0',
      u'to_user_name': None},
     {u'_id': ObjectId('50f99bf66577e466cf550b35'),
      u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1),
      u'from_user': u'ibmmb',
      u'from_user_id': 115674359,
      u'from_user_id_str': u'115674359',
      u'from_user_name': u'Maarten Boerma',
      u'geo': None,
      u'id': 292341338798690304L,
      u'iso_language_code': u'en',
      u'source': u'web',
      u'text': u'RT @IBMcloud: Big data in the #cloud? Governing a sprawling business resource http://t.co/FDsoNfrf via @jameskobielus #bigdata',
      u'to_user': None,
      u'to_user_id': 0,
      u'to_user_id_str': u'0',
      u'to_user_name': None}]
</pre>


## Counting

If we just want to know how many documents match a query we can perform a count() operation instead of a full query. We can get a count of all of the documents in a collection:

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    149
</pre>


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">()</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    149
</pre>


## Query Operators

MongoDB queries are represented as JSON-like structure, just like documents. To build a query, you just need to specify a dictionary with the properties you wish the results to match. For example, this query will match all documents in the posts collection with ISO language code "en".

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:</span> <span class="s">&quot;en&quot;</span><span class="p">})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    126
</pre>


If we wanted to retrieve all documents with ISO language code "en" and source equal to "twitterfeed":

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:</span><span class="s">&quot;en&quot;</span><span class="p">,</span><span class="s">&quot;source&quot;</span><span class="p">:</span><span class="s">&quot;twitterfeed&quot;</span><span class="p">})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    5
</pre>


Queries can also use special query operators. These operators include **gt, gte, lt, lte, ne, nin, regex, exists, not, or**, and many more. The following queries show the use of some of these operators.

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">datetime</span> <span class="kn">import</span> <span class="n">datetime</span>
<span class="c"># cheat: year, month, day, hour, minute, second, microsecond</span>
<span class="n">date1</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">strptime</span><span class="p">(</span><span class="s">&quot;18/01/13 18:30&quot;</span><span class="p">,</span> <span class="s">&quot;</span><span class="si">%d</span><span class="s">/%m/%y %H:%M&quot;</span><span class="p">)</span>
<span class="n">date2</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">strptime</span><span class="p">(</span><span class="s">&quot;18/01/13 18:05&quot;</span><span class="p">,</span> <span class="s">&quot;</span><span class="si">%d</span><span class="s">/%m/%y %H:%M&quot;</span><span class="p">)</span>
<span class="n">date3</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">strptime</span><span class="p">(</span><span class="s">&quot;18/01/13 18:10&quot;</span><span class="p">,</span> <span class="s">&quot;</span><span class="si">%d</span><span class="s">/%m/%y %H:%M&quot;</span><span class="p">)</span>
<span class="n">date4</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">strptime</span><span class="p">(</span><span class="s">&quot;18/01/13 18:25&quot;</span><span class="p">,</span> <span class="s">&quot;</span><span class="si">%d</span><span class="s">/%m/%y %H:%M&quot;</span><span class="p">)</span>

<span class="n">cursor</span> <span class="o">=</span> <span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&#39;created_at&#39;</span><span class="p">:{</span><span class="s">&quot;$gt&quot;</span><span class="p">:</span><span class="n">date1</span><span class="p">}})</span>
<span class="n">cursor</span><span class="o">.</span><span class="n">next</span><span class="p">()</span>
</pre></div>


<pre>
    {u'_id': ObjectId('50f99bf66577e466cf550b34'),
     u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1),
     u'from_user': u'BITechWatch',
     u'from_user_id': 22631958,
     u'from_user_id_str': u'22631958',
     u'from_user_name': u'Marly Cho',
     u'geo': None,
     u'id': 292341338840653825L,
     u'iso_language_code': u'en',
     u'source': u'twitterfeed',
     u'text': u"Everything you ever wanted to know about R functions: It's hard to overstate the importance of function... http://t.co/sD5bG4yg #bigdata",
     u'to_user': None,
     u'to_user_id': 0,
     u'to_user_id_str': u'0',
     u'to_user_name': None}
</pre>


This time we will do the same query but add the count() method to only get the count of documents that match the query. We will use count() from now onwards (easier!!!)

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&#39;created_at&#39;</span><span class="p">:{</span><span class="s">&quot;$gt&quot;</span><span class="p">:</span><span class="n">date1</span><span class="p">}})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    44
</pre>


<div class="highlight"><pre><span class="c"># Tweets dates low than or equal to date2</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&#39;created_at&#39;</span><span class="p">:{</span><span class="s">&quot;$lte&quot;</span><span class="p">:</span><span class="n">date2</span><span class="p">}})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    14
</pre>


<div class="highlight"><pre><span class="c"># Between 2 dates</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;created_at&quot;</span><span class="p">:</span> <span class="p">{</span><span class="s">&quot;$gte&quot;</span><span class="p">:</span> <span class="n">date3</span><span class="p">,</span> <span class="s">&quot;$lt&quot;</span><span class="p">:</span> <span class="n">date4</span><span class="p">}})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    52
</pre>


<div class="highlight"><pre><span class="c"># Posts in either spanish or french</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:{</span><span class="s">&quot;$in&quot;</span><span class="p">:[</span><span class="s">&quot;es&quot;</span><span class="p">,</span><span class="s">&quot;fr&quot;</span><span class="p">]}})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    7
</pre>


<div class="highlight"><pre><span class="c"># Posts in either spanish or french using $or</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;$or&quot;</span><span class="p">:[{</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:</span><span class="s">&quot;es&quot;</span><span class="p">},{</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:</span><span class="s">&quot;fr&quot;</span><span class="p">}]})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    7
</pre>


<div class="highlight"><pre><span class="c"># All posts except spanish or french</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:{</span><span class="s">&quot;$nin&quot;</span><span class="p">:[</span><span class="s">&quot;es&quot;</span><span class="p">,</span><span class="s">&quot;fr&quot;</span><span class="p">]}})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    142
</pre>


<div class="highlight"><pre><span class="c"># Using Regex to find a post with hashtag #analytics</span>
<span class="kn">import</span> <span class="nn">re</span>
<span class="n">regex</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s">r&#39;#analytics&#39;</span><span class="p">)</span>
<span class="n">rstats</span> <span class="o">=</span> <span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;text&quot;</span><span class="p">:</span><span class="n">regex</span><span class="p">})</span>
<span class="n">rstats</span>
</pre></div>


<pre>
    {u'_id': ObjectId('50f99bf66577e466cf550b3b'),
     u'created_at': datetime.datetime(2013, 1, 18, 18, 41, 23),
     u'from_user': u'DGleebits',
     u'from_user_id': 364557525,
     u'from_user_id_str': u'364557525',
     u'from_user_name': u'Dan Gleebits ',
     u'geo': None,
     u'id': 292340928268623872L,
     u'iso_language_code': u'en',
     u'source': u'Tweet Button',
     u'text': u'LazyWeb Reblog of Big Data Security Challenges http://t.co/vAY5CVOz via @wordpressdotcom #infosec #dfir #bigdata #analytics',
     u'to_user': None,
     u'to_user_id': 0,
     u'to_user_id_str': u'0',
     u'to_user_name': None}
</pre>


We'll cover other operators further down once we have covered the Update process.

## Sorting Documents

MongoDB can sort query results for you on the server-side. Especially if you are sorting results on a property which has an index, it can sort these far more efficiently than your client program can.

Here's an exmaple of using a descending sort to get the last tweet in our collection.

<div class="highlight"><pre><span class="n">lastTweet</span> <span class="o">=</span> <span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">()</span><span class="o">.</span><span class="n">sort</span><span class="p">([(</span><span class="s">&quot;created_at&quot;</span><span class="p">,</span> <span class="n">pymongo</span><span class="o">.</span><span class="n">DESCENDING</span><span class="p">)])</span>
<span class="n">lastTweet</span><span class="o">.</span><span class="n">next</span><span class="p">()</span>
</pre></div>


<pre>
    {u'_id': ObjectId('50f99bf66577e466cf550b34'),
     u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1),
     u'from_user': u'BITechWatch',
     u'from_user_id': 22631958,
     u'from_user_id_str': u'22631958',
     u'from_user_name': u'Marly Cho',
     u'geo': None,
     u'id': 292341338840653825L,
     u'iso_language_code': u'en',
     u'source': u'twitterfeed',
     u'text': u"Everything you ever wanted to know about R functions: It's hard to overstate the importance of function... http://t.co/sD5bG4yg #bigdata",
     u'to_user': None,
     u'to_user_id': 0,
     u'to_user_id_str': u'0',
     u'to_user_name': None}
</pre>


What about the first tweet in french?

<div class="highlight"><pre><span class="n">frlastTweet</span> <span class="o">=</span> <span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;iso_language_code&quot;</span><span class="p">:</span><span class="s">&quot;fr&quot;</span><span class="p">})</span><span class="o">.</span><span class="n">sort</span><span class="p">([(</span><span class="s">&quot;created_at&quot;</span><span class="p">,</span> <span class="n">pymongo</span><span class="o">.</span><span class="n">ASCENDING</span><span class="p">)])</span>
<span class="n">frlastTweet</span><span class="o">.</span><span class="n">next</span><span class="p">()</span>
</pre></div>


<pre>
    {u'_id': ObjectId('50f99bf66577e466cf550b99'),
     u'created_at': datetime.datetime(2013, 1, 18, 18, 13, 52),
     u'from_user': u'jbmgrtn',
     u'from_user_id': 87185256,
     u'from_user_id_str': u'87185256',
     u'from_user_name': u'J\xe9r\xf4me Baumgarten',
     u'geo': None,
     u'id': 292334004466761729L,
     u'iso_language_code': u'fr',
     u'source': u'Twitter for iPhone',
     u'text': u'@jhattat la pr\xe9s dont je parlais sur BigData et Hadoop http://t.co/4McdjN80',
     u'to_user': u'jhattat',
     u'to_user_id': 24175910,
     u'to_user_id_str': u'24175910',
     u'to_user_name': u'J\xe9r\xe9mie HATTAT'}
</pre>


The above queries are not very optimal when you have large result sets. Pymongo have a limit() method which let you fetch a limited number of results.

<div class="highlight"><pre><span class="n">lastTweetOnly</span> <span class="o">=</span> <span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">()</span><span class="o">.</span><span class="n">sort</span><span class="p">([(</span><span class="s">&quot;created_at&quot;</span><span class="p">,</span> <span class="n">pymongo</span><span class="o">.</span><span class="n">DESCENDING</span><span class="p">)])</span><span class="o">.</span><span class="n">limit</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>
<span class="k">for</span> <span class="n">t</span> <span class="ow">in</span> <span class="n">lastTweetOnly</span><span class="p">:</span> <span class="k">print</span> <span class="n">t</span>
</pre></div>


    {u'iso_language_code': u'en', u'to_user_name': None, u'created_at': datetime.datetime(2013, 1, 18, 18, 43, 1), u'text': u"Everything you ever wanted to know about R functions: It's hard to overstate the importance of function... http://t.co/sD5bG4yg #bigdata", u'from_user_id_str': u'22631958', u'to_user_id_str': u'0', u'to_user': None, u'source': u'twitterfeed', u'to_user_id': 0, u'from_user': u'BITechWatch', u'id': 292341338840653825L, u'from_user_id': 22631958, u'_id': ObjectId('50f99bf66577e466cf550b34'), u'geo': None, u'from_user_name': u'Marly Cho'}


## Updating Documents

PyMongo can update documents in a number of different ways. Let's start for adding a new document to our collection.


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">,</span><span class="s">&quot;created_at&quot;</span><span class="p">:</span><span class="n">datetime</span><span class="p">(</span><span class="mi">2013</span><span class="p">,</span><span class="mi">1</span><span class="p">,</span><span class="mi">21</span><span class="p">,</span><span class="mi">15</span><span class="p">,</span><span class="mi">27</span><span class="p">,</span><span class="mi">59</span><span class="p">),</span><span class="s">&quot;text&quot;</span><span class="p">:</span><span class="s">&quot;Hello World&quot;</span><span class="p">,</span> <span class="s">&quot;from_user&quot;</span><span class="p">:</span><span class="s">&quot;Altons&quot;</span><span class="p">,</span><span class="s">&quot;source&quot;</span><span class="p">:</span><span class="s">&quot;Ipython&quot;</span><span class="p">})</span>
</pre></div>


<pre>
    1234
</pre>


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'created_at': datetime.datetime(2013, 1, 21, 15, 27, 59),
     u'from_user': u'Altons',
     u'source': u'Ipython',
     u'text': u'Hello World'}
</pre>


Now we can use the update() method to modify the document. This operation finds the document we just inserted by _id and updates it with a new document.

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;from_user&quot;</span><span class="p">:</span><span class="s">&quot;anonymous&quot;</span><span class="p">})</span>

<span class="c">#Fetch our updated document</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234, u'from_user': u'anonymous'}
</pre>


The update() method replaces the whole document so be careful! If instead we want to modify specific fields of the document we can use MongoDB's update operators like **set, inc, push, pull** and many more.

### Update Operator: set

This statement updates in the document in collection where field matches value1 by replacing the value of the field field1 with value2. This operator will add the specified field or fields if they do not exist in this document or replace the existing value of the specified field(s) if they already exist.

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$set&quot;</span><span class="p">:{</span><span class="s">&quot;from_user&quot;</span><span class="p">:</span><span class="s">&quot;Altons&quot;</span><span class="p">,</span><span class="s">&quot;source&quot;</span><span class="p">:</span><span class="s">&quot;Ipython notebook&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234, u'from_user': u'Altons', u'source': u'Ipython notebook'}
</pre>


**Upsert**

An **upsert** eliminates the need to perform a separate database call to check for the existence of a record before performing either an update or an insert operation. Typically update operations update existing documents, but in MongoDB, the update() operation can accept an **upsert** option as an argument. Upserts are a hybrid operation that use the **query** argument to determine the write operation:

- If the query matches an existing document(s), the upsert performs an update.
- If the query matches no document in the collection, the upsert inserts a single document.

Let's see an example:

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">},{</span><span class="s">&quot;$set&quot;</span><span class="p">:{</span><span class="s">&quot;from_user&quot;</span><span class="p">:</span><span class="s">&quot;Alberto&quot;</span><span class="p">,</span><span class="s">&quot;source&quot;</span><span class="p">:</span><span class="s">&quot;unavailable&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    0
</pre>


The update fails because no document matched the query for the update. But using upsert will sort this out:

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">},{</span><span class="s">&quot;$set&quot;</span><span class="p">:{</span><span class="s">&quot;from_user&quot;</span><span class="p">:</span><span class="s">&quot;Alberto&quot;</span><span class="p">,</span><span class="s">&quot;source&quot;</span><span class="p">:</span><span class="s">&quot;unavailable&quot;</span><span class="p">}},</span> <span class="n">upsert</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    1
</pre>


**multi=True**

By default MongoDB only modifies the first document that matches the query. If you want to modify all documents that match the query add multi=True.

### Update Operator: inc

The inc operator increments a value by a specified amount if field is present in the document. If the field does not exist, $inc sets field to the number value. For example:

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$set&quot;</span><span class="p">:{</span><span class="s">&quot;total_posts&quot;</span><span class="p">:</span><span class="mi">1</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'from_user': u'Altons',
     u'source': u'Ipython notebook',
     u'total_posts': 1}
</pre>


<div class="highlight"><pre><span class="c"># Increment total_posts by 9 tweets</span>
<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$inc&quot;</span><span class="p">:{</span><span class="s">&quot;total_posts&quot;</span><span class="p">:</span><span class="mi">9</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'from_user': u'Altons',
     u'source': u'Ipython notebook',
     u'total_posts': 10}
</pre>


###Update Operator: unset

The unset operator deletes a particular field. If documents match the initial query but do not have the field specified in the unset operation, there the statement has no effect on the document.



<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$unset&quot;</span><span class="p">:{</span><span class="s">&quot;total_posts&quot;</span><span class="p">:</span><span class="s">&quot;&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234, u'from_user': u'Altons', u'source': u'Ipython notebook'}
</pre>


### Update Operator: rename

The rename operator updates the name of a field. The new field name must differ from the existing field name.

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$rename&quot;</span><span class="p">:{</span><span class="s">&quot;from_user&quot;</span><span class="p">:</span><span class="s">&quot;username&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234, u'source': u'Ipython notebook', u'username': u'Altons'}
</pre>


Here we have a good opportunity to see **exists** in action (it should return only 1 as there only one document with field **username**):

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find</span><span class="p">({</span><span class="s">&quot;username&quot;</span><span class="p">:{</span><span class="s">&quot;$exists&quot;</span><span class="p">:</span><span class="bp">True</span><span class="p">}})</span><span class="o">.</span><span class="n">count</span><span class="p">()</span>
</pre></div>


<pre>
    1
</pre>


### Update Operator: push 

The **push** operator appends a specified value to an array.Be aware of the following behaviors:

- If the field specified in the **push** statement (e.g. { $push: { field: value1 } }) does not exist in the matched document, the operation adds a new array with the specified field and value (e.g. value1) to the matched document.
- The operation will fail if the field specified in the **push** statement is not an array. $push does not fail when pushing a value to a non-existent field.
- If value1 is an array itself, **push** appends the whole array as an element in the identified array. To add multiple items to an array, use [pushAll](http://docs.mongodb.org/manual/reference/operator/pushAll/#_S_pushAll).

Now for this example, let's say we have 2 predictive models that score the sentiment of each tweet in the range -5,5 (-5 = worse, 0 = neutral and 5=best) and we want to add those scores to each document.

Let's use our well known document _id=1234

<div class="highlight"><pre><span class="kn">import</span> <span class="nn">random</span>

<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$push&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:{</span><span class="s">&quot;nb&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">),</span><span class="s">&quot;svm&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">)}}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': 0, u'svm': -2}],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


In the above example we have added scores to document 1234, let's see what happens if we run the same code again.

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$push&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:{</span><span class="s">&quot;nb&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">),</span><span class="s">&quot;svm&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">)}}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': 0, u'svm': -2}, {u'nb': 1, u'svm': 4}],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


it will add another array as expected. I don't know why one would think it will update the original array instead of appending a new one. So don't make the mistake I did!

if you run it twice or more you always have the **unset** operator to the rescue (if you want to start from scratch!)

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$unset&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:</span><span class="s">&quot;&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234, u'source': u'Ipython notebook', u'username': u'Altons'}
</pre>


### Update Operator: pop

The **pop** operator removes the first or last element of an array. Pass **pop** a value of 1 to remove the last element in an array and a value of -1 to remove the first element of an array.

Be aware of the following **pop** behaviors:

- The **pop** operation fails if field is not an array.
- **pop** will successfully remove the last item in an array. field will then hold an empty array.

We can use **pop** if we don't want to start (or can't) from scratch:

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$push&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:{</span><span class="s">&quot;nb&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">),</span><span class="s">&quot;svm&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">)}}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$push&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:{</span><span class="s">&quot;nb&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">),</span><span class="s">&quot;svm&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">)}}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': -5, u'svm': 0}, {u'nb': 4, u'svm': 2}],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$pop&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:</span><span class="mi">1</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': -5, u'svm': 0}],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


### Update Operator: pull

The **pull** operator removes all instances of a value from an existing array. If the value existed multiple times in the field array, **pull** would remove all instances of this value in this array.

It is very handy when you exactly what value you want to remove.

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">},{</span><span class="s">&quot;$set&quot;</span><span class="p">:{</span><span class="s">&quot;skills&quot;</span><span class="p">:[</span><span class="s">&quot;python&quot;</span><span class="p">,</span><span class="s">&quot;SAS&quot;</span><span class="p">,</span><span class="s">&quot;R&quot;</span><span class="p">,</span><span class="s">&quot;javascript&quot;</span><span class="p">,</span><span class="s">&quot;java&quot;</span><span class="p">]}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 5678,
     u'from_user': u'Alberto',
     u'skills': [u'python', u'SAS', u'R', u'javascript', u'java'],
     u'source': u'unavailable'}
</pre>


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">},{</span><span class="s">&quot;$pull&quot;</span><span class="p">:{</span><span class="s">&quot;skills&quot;</span><span class="p">:</span><span class="s">&quot;java&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 5678,
     u'from_user': u'Alberto',
     u'skills': [u'python', u'SAS', u'R', u'javascript'],
     u'source': u'unavailable'}
</pre>


### Update Operator: addToSet

The **addToSet** operator adds a value to an array only if the value is not in the array already. If the value is in the array, **addToSet** returns without modifying the array. Otherwise, **addToSet** behaves the same as **push**

<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 5678,
     u'from_user': u'Alberto',
     u'skills': [u'python', u'SAS', u'R', u'javascript'],
     u'source': u'unavailable'}
</pre>


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">},{</span><span class="s">&quot;$addToSet&quot;</span><span class="p">:{</span><span class="s">&quot;skills&quot;</span><span class="p">:</span><span class="s">&quot;python&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 5678,
     u'from_user': u'Alberto',
     u'skills': [u'python', u'SAS', u'R', u'javascript'],
     u'source': u'unavailable'}
</pre>


<div class="highlight"><pre><span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">},{</span><span class="s">&quot;$addToSet&quot;</span><span class="p">:{</span><span class="s">&quot;skills&quot;</span><span class="p">:</span><span class="s">&quot;Perl&quot;</span><span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 5678,
     u'from_user': u'Alberto',
     u'skills': [u'python', u'SAS', u'R', u'javascript', u'Perl'],
     u'source': u'unavailable'}
</pre>


###Update Operator: $

The positional $ operator identifies an element in an array field to update without explicitly specifying the position of the element in the array. The positional operator, when used with the update() method and acts as a placeholder for the first match of the update query selector.

<div class="highlight"><pre><span class="c"># sample document</span>
<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$set&quot;</span><span class="p">:{</span><span class="s">&quot;skills&quot;</span><span class="p">:[</span><span class="s">&quot;python&quot;</span><span class="p">,</span><span class="s">&quot;SAS&quot;</span><span class="p">,</span><span class="s">&quot;R&quot;</span><span class="p">,</span><span class="s">&quot;javascript&quot;</span><span class="p">,</span><span class="s">&quot;java&quot;</span><span class="p">]}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': -5, u'svm': 0}],
     u'skills': [u'python', u'SAS', u'R', u'javascript', u'java'],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


<div class="highlight"><pre><span class="c"># update R to Rstats</span>
<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">,</span><span class="s">&quot;skills&quot;</span><span class="p">:</span><span class="s">&quot;R&quot;</span><span class="p">},{</span> <span class="s">&quot;$set&quot;</span><span class="p">:</span> <span class="p">{</span> <span class="s">&quot;skills.$&quot;</span> <span class="p">:</span> <span class="s">&quot;Rstats&quot;</span> <span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': -5, u'svm': 0}],
     u'skills': [u'python', u'SAS', u'Rstats', u'javascript', u'java'],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


<div class="highlight"><pre><span class="c"># Another example</span>
<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">},{</span><span class="s">&quot;$push&quot;</span><span class="p">:{</span><span class="s">&quot;sentiment&quot;</span><span class="p">:{</span><span class="s">&quot;nb&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">),</span><span class="s">&quot;svm&quot;</span><span class="p">:</span><span class="n">random</span><span class="o">.</span><span class="n">randint</span><span class="p">(</span><span class="o">-</span><span class="mi">5</span><span class="p">,</span> <span class="mi">5</span><span class="p">)}}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': -5, u'svm': 0}, {u'nb': 1, u'svm': 4}],
     u'skills': [u'python', u'SAS', u'Rstats', u'javascript', u'java'],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


<div class="highlight"><pre><span class="c"># Use the positional $ operator to update the value of the nb field to zero in the embedded document with the svm of 4:</span>
<span class="n">posts</span><span class="o">.</span><span class="n">update</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">,</span><span class="s">&quot;sentiment.svm&quot;</span><span class="p">:</span><span class="mi">4</span><span class="p">},{</span> <span class="s">&quot;$set&quot;</span><span class="p">:</span> <span class="p">{</span> <span class="s">&quot;sentiment.$.nb&quot;</span> <span class="p">:</span> <span class="mi">0</span> <span class="p">}})</span>
<span class="n">posts</span><span class="o">.</span><span class="n">find_one</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">1234</span><span class="p">})</span>
</pre></div>


<pre>
    {u'_id': 1234,
     u'sentiment': [{u'nb': -5, u'svm': 0}, {u'nb': 0, u'svm': 4}],
     u'skills': [u'python', u'SAS', u'Rstats', u'javascript', u'java'],
     u'source': u'Ipython notebook',
     u'username': u'Altons'}
</pre>


## Removing Data

Removing databases, collections and documents in Pymongo is a straight forward process:


<div class="highlight"><pre><span class="n">conn</span><span class="o">.</span><span class="n">database_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'sandpit-test', u'twitter_results', u'local']
</pre>


<div class="highlight"><pre><span class="c"># Remove database sandpit-test</span>
<span class="n">conn</span><span class="o">.</span><span class="n">drop_database</span><span class="p">(</span><span class="s">&quot;sandpit-test&quot;</span><span class="p">)</span>
<span class="n">conn</span><span class="o">.</span><span class="n">database_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'twitter_results', u'local']
</pre>


<div class="highlight"><pre><span class="c"># Create a database, then a collection and a dummy document</span>
<span class="n">conn</span><span class="o">.</span><span class="n">dummy</span><span class="o">.</span><span class="n">dummy_collection</span><span class="o">.</span><span class="n">insert</span><span class="p">({</span><span class="s">&quot;greeting&quot;</span><span class="p">:</span><span class="s">&quot;Hello World&quot;</span><span class="p">})</span>
<span class="n">conn</span><span class="o">.</span><span class="n">dummy</span><span class="o">.</span><span class="n">collection_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'system.indexes', u'dummy_collection']
</pre>


<div class="highlight"><pre><span class="n">conn</span><span class="o">.</span><span class="n">dummy</span><span class="o">.</span><span class="n">collection_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'system.indexes', u'dummy_collection']
</pre>


<div class="highlight"><pre><span class="c"># Delete a collection</span>
<span class="n">conn</span><span class="o">.</span><span class="n">dummy</span><span class="o">.</span><span class="n">drop_collection</span><span class="p">(</span><span class="s">&quot;dummy_collection&quot;</span><span class="p">)</span>
<span class="n">conn</span><span class="o">.</span><span class="n">dummy</span><span class="o">.</span><span class="n">collection_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'system.indexes']
</pre>


<div class="highlight"><pre><span class="c"># Delete dummy database</span>
<span class="n">conn</span><span class="o">.</span><span class="n">drop_database</span><span class="p">(</span><span class="s">&quot;dummy&quot;</span><span class="p">)</span>
<span class="n">conn</span><span class="o">.</span><span class="n">database_names</span><span class="p">()</span>
</pre></div>


<pre>
    [u'twitter_results', u'local']
</pre>


<div class="highlight"><pre><span class="c"># Remove documents.</span>
<span class="c">#  Please note that there is no multi=True option for remove. MongoDB will remove any documents that match the query</span>
<span class="n">posts</span><span class="o">.</span><span class="n">remove</span><span class="p">({</span><span class="s">&quot;_id&quot;</span><span class="p">:</span><span class="mi">5678</span><span class="p">})</span>
</pre></div>


<pre>
    {u'connectionId': 5, u'err': None, u'n': 1, u'ok': 1.0}
</pre>


If we don't specify what documents to remove MongoDB will remove them all. This just removes the documents. The collection and its indexes still exist.

## Useful Commands

If you need to get some statistics about your collections.

<div class="highlight"><pre><span class="n">db</span><span class="o">.</span><span class="n">command</span><span class="p">({</span><span class="s">&#39;dbstats&#39;</span><span class="p">:</span> <span class="mi">1</span><span class="p">})</span>
</pre></div>


<pre>
    {u'avgObjSize': 400.46753246753246,
     u'collections': 3,
     u'dataSize': 61672,
     u'db': u'twitter_results',
     u'fileSize': 201326592,
     u'indexSize': 8176,
     u'indexes': 1,
     u'nsSizeMB': 16,
     u'numExtents': 4,
     u'objects': 154,
     u'ok': 1.0,
     u'storageSize': 155648}
</pre>


To get collection statistics use the collstats command:

<div class="highlight"><pre><span class="n">db</span><span class="o">.</span><span class="n">command</span><span class="p">({</span><span class="s">&#39;collstats&#39;</span><span class="p">:</span> <span class="s">&#39;posts&#39;</span><span class="p">})</span>
</pre></div>


<pre>
    {u'avgObjSize': 409.76,
     u'count': 150,
     u'indexSizes': {u'_id_': 8176},
     u'lastExtentSize': 114688,
     u'nindexes': 1,
     u'ns': u'twitter_results.posts',
     u'numExtents': 2,
     u'ok': 1.0,
     u'paddingFactor': 1.0000000000000004,
     u'size': 61464,
     u'storageSize': 143360,
     u'systemFlags': 1,
     u'totalIndexSize': 8176,
     u'userFlags': 0}
</pre>


## Things I did not covered in this tutorial

- [Aggregation Framework](http://docs.mongodb.org/manual/reference/aggregation/) (Still chinese to me).
- [Map Reduce](http://docs.mongodb.org/manual/applications/map-reduce/)
- [GridFS](http://docs.mongodb.org/manual/applications/gridfs/)
- [Journaling](http://docs.mongodb.org/manual/administration/journaling/) 

I hope you find this tutorial useful. I'll be using it as my online cheat sheet! 
