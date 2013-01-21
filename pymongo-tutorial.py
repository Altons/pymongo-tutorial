# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# I use [mongoDB](http://www.mongodb.org/) along with [Pymongo](http://api.mongodb.org/python/current/) for personal projects only (I hope this changes in the near future though) and not very often to be honest. So this post is more of a quick reference for myself and I hope you guys finds it useful too. I am also writing this post in [Ipython](http://ipython.org/) which I will convert to [markdown](http://en.wikipedia.org/wiki/Markdown) using [nbconvert utility](http://blog.fperez.org/2012/09/blogging-with-ipython-notebook.html) and then push it to my github blog using [Jekyll](http://jekyllbootstrap.com/). Fingers crossed it won't be too difficult.
# 
# For this tutorial I'll be using real data from Twitter using the [Tweepy](https://github.com/tweepy/tweepy) package.
# 
# Before we start let's see what Wikipedia has to say about MongoDB:
# 
# > "MongoDB (from "humongous") is an open source document-oriented database system developed and supported by 10gen. It is part of the NoSQL family of database systems. Instead of storing data in tables as is done in a "classical" relational database, MongoDB stores structured data as JSON-like documents with dynamic schemas (MongoDB calls the format BSON), making the integration of data in certain types of applications easier and faster.
# 
# >10gen began Development of MongoDB in October 2007. The database is used by MTV Networks, Craigslist, Foursquare and UIDAI Aadhaar. MongoDB is the most popular NoSQL database management system."
# 
# Done - let's start!
# 
# ## Downloading & Installing MongoDB binaries
# 
# 1. Head to the MongoDB download page [http://www.mongodb.org/downloads](http://www.mongodb.org/downloads) and get version 2.2.2 (or latest stable version) for your OS (*by the way I'm using OSX for this tutorial so \*nix guys should have no difficulty following along but Windows users may need to change some bits - sorry!*).
# 
# 2. Unzip mongodb-osx-x86_64-2.2.2.tgz and rename folder mongodb-osx-x86_64-2.2.2 to simply mongodb. I normally move this folder to my personal project folder so feel free to move it in wherever you like. Your mongodb folder should have the following structure: 
# `
# altons@asgard:~/projects$ls -R mongodb
# GNU-AGPL-3.0        README              THIRD-PARTY-NOTICES bin
# mongodb/bin:
# bsondump     mongod       mongoexport  mongoimport  mongoperf    mongos       mongostat
# mongo        mongodump    mongofiles   mongooplog   mongorestore mongosniff   mongotop
# altons@asgard:~/projects$
# `
# 3. Kick off the mongodb server:
# `
# altons@asgard:~/projects$ cd mongodb
# altons@asgard:~/projects/mongodb$./bin/mongod --dbpath . --nojournal &
# `
# 4. Open another terminal windows and type: `altons@asgard:~/projects/mongodb$./bin/mongo`
# 
# if you something like:
# `
# MongoDB shell version: 2.2.2
# connecting to: test
# Welcome to the MongoDB shell.
# For interactive help, type "help".
# For more comprehensive documentation, see
# 	http://docs.mongodb.org/
# Questions? Try the support group
# 	http://groups.google.com/group/mongodb-user
# > 
# `
# then you are good to go! Type **exit** to quit and go to the previous terminal windows and hit Ctrl+C to kill the server  - we need a bit of customization first.
# 
# **Note**: Sometimes (with God as my witness!) Ctrl-C doesn't kill the server and I have to do a `kill -9` on the pid where mongod still running. If that happens - you also need to remove mongodb.lock from your **dbpath** manually otherwise mongoDB will complain next time you fire it up.
# 
# ## The config file
# 
# The option --dbpath . will save your data inside the mongodb folder - I am not a huge fan of this option. I like to keep my data separated from db binaries. So instead I'll use a config file to tell mongoDB where to store my data.
# 
# Here it is my config file:
# `
# # Mongo Production server configuration
# # Author: Alberto Negron
# # created on: 26/07/2012
# 
# dbpath=/Users/altons/projects/data/mongodb/                         # location where I want to store my databases - Use full path
# port = 27017                                                        # default port
# bind_ip = 127.0.0.1                                                 # default ip
# logpath = /Users/altons/projects/data/mongodb/log/mongodb.log       # location where I want to store logs - Use full path
# logappend = true                                                    # everytime I fire up mongodb the new log will be appended to a master log file
# rest=true                                                           # this option let you check server status at http:\\127.0.0.1:27017
# directoryperdb = true                                               # Set to true to modify the storage pattern of the data directory to store each database’s
#                                                                     # files in a distinct folder. This option will create directories within the dbpath 
#                                                                     # named for each directory
# 
# `
# and I have saved it as mongo.conf in side the data folder ` (~/projects/data) `.
# 
# Now go back to the mongodb folder and use the following command to fire up the server:
# 
# `
# altons@asgard:~/projects/mongodb$./bin/mongod --config=/Users/altons/projects/data/mongo.conf  --nojournal &
# `
# 
# Since the option rest is set to true you can check mongodb status via [http://127.0.0.1:28017/](http://127.0.0.1:28017/)
# 
# You can have  multiple config files (Prod/Dev/Test) or any combination of servers running on different ports. Options are endless.
# 
# ## Pymongo
# 
# PyMongo is a Python distribution containing tools for working with MongoDB, and is the recommended way to work with MongoDB from Python. You can install mongodb from either pip or easy_install.
# 
# ### Connecting to MongoDB

# <markdowncell>

# In Pymongo 2.4.1 the connection method has been deprecated. Now we most use MongoClient

# <codecell>

import pymongo

# Connection to Mongo DB
try:
    conn=pymongo.MongoClient()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 
conn

# <markdowncell>

# We are now connected to our server.
# 
# ### Databases
# 
# Mongodb creates databases and collections automatically for you if they don't exist already. A single instance of MongoDB can support multiple independent databases. When working with PyMongo you access databases using attribute style access:

# <codecell>

db = conn.mydb
db

# <markdowncell>

# If your database name is such that using attribute style access won’t work (like db-name), you can use dictionary style access instead:

# <codecell>

db = conn['sandpit-test']
db

# <markdowncell>

# If you need to know what databases are available:

# <codecell>

conn.database_names()

# <markdowncell>

# We already created 2 new databases. Why didn't show up with the above command? Well, databases with no collections or with empty collections will not show up with database_names(). Same goes when we try to list empty collections in a database.
# 
# We'll test it again once we have populate some collections.
# 
# ### Collections
# 
# A collection is a group of documents stored in MongoDB, and can be thought of as roughly the equivalent of a table in a relational database. Getting a collection in PyMongo works the same as getting a database:

# <codecell>

collection = db.my_collection
collection

# <codecell>

db.collection_names()

# <markdowncell>

# However one must be careful when trying to get existing collections. For example, if you a collection db.user and you type db.usr this is clearly a typo. Unlike an RDBMS, MongoDB won't protect you from this class of mistake.
# 
# 
# ### Documents
# 
# MongoDB stores structured data as JSON-like documents, using dynamic schemas (called BSON), rather than predefined schemas. An element of data is called a document, and documents are stored in collections. One collection may have any number of documents.
# 
# Compared to relational databases, we could say collections are like tables, and documents are like records. But there is one big difference: every record in a table has the same fields (with, usually, differing values) in the same order, while each document in a collection can have completely different fields from the other documents. 
# 
# All you really need to know when you're using Python, however, is that documents are Python dictionaries that can have strings as keys and can contain various primitive types (int, float,unicode, datetime) as well as other documents (Python dicts) and arrays (Python lists).
# 
# To insert some data into MongoDB, all we need to do is create a dict and call .insert() on the collection object:
# 

# <codecell>

doc = {"name":"Alberto","surname":"Negron","twitter":"@Altons"}

# <markdowncell>

# Now we need to insert the above document into a collection:

# <codecell>

collection.insert(doc)

# <markdowncell>

# Congratulations you have created your first document!!

# <codecell>

conn.database_names()

# <codecell>

db.collection_names()

# <markdowncell>

#  Now database_names() and collection_names() show database **sandpit-test** and collection **my_collection**.
# 
# To recap, we have **databases** containing **collections**. A **collection** is made up of **documents**. Each document is made up of **fields**.
# 
# 
# ## Tweepy
# 
# Before continue with the tutorial, let's get some real data from twitter and insert it in a new database - it'll be definitely more interesting!!!
# 
# Let's pull the first 10 result pages with the keyword 'BigData'

# <codecell>

from tweepy import API

# <codecell>

lookup ='BigData'
api = API()

search = []
page = 1
maxPage = 10
while(page<=maxPage):
    tweets = api.search(lookup,page = page)
    for tweet in tweets:
        search.append(tweet)
    page = page + 1

# <markdowncell>

# Let's how many tweets we got from the above search:

# <codecell>

len(search)

# <markdowncell>

# Not bad, let inspect the structure of the first object:

# <codecell>

dir(search[0])

# <markdowncell>

# There is a lot of information that we really don't need. Let's keep only the data related to the tweet and insert it into MongoDB

# <codecell>

# Define my mongoDB database
db = conn.twitter_results
# Define my collection where I'll insert my search
posts = db.posts

# <codecell>



# loop through search and insert dictionary into mongoDB
for tweet in search:
    # Empty dictionary for storing tweet related data
    data ={}
    data['created_at'] = tweet.created_at
    data['from_user'] = tweet.from_user
    data['from_user_id'] = tweet.from_user_id
    data['from_user_id_str'] = tweet.from_user_id_str
    data['from_user_name'] = tweet.from_user_name
    data['geo'] = tweet.geo
    data['id'] = tweet.id
    data['iso_language_code'] = tweet.iso_language_code
    data['source'] = tweet.source
    data['text'] = tweet.text
    data['to_user'] = tweet.to_user
    data['to_user_id'] = tweet.to_user_id
    data['to_user_id_str'] = tweet.to_user_id_str
    data['to_user_name'] = tweet.to_user_name
    # Insert process
    posts.insert(data)
    

# <markdowncell>

# Dead easy! we have created our collection of tweets, no need to define table and columns beforehand - that's the beauty of MongoDB.
# 
# Here it is the structure of the last document inserted:

# <codecell>

data 

# <markdowncell>

# #### The _id field
# 
# 
# In MongoDB, documents stored in a collection require a unique _id field that acts as a primary key. Because ObjectIds are small, most likely unique, and fast to generate, MongoDB uses ObjectIds as the default value for the _id field if the _id field is not specified; i.e., the mongod adds the _id field and generates a unique ObjectId to assign as its value
# 
# ## Reading Documents in a Collection
# 
# The first and foremost important operation we need to learn is how to retrieve our data from MongoDB. For this, Collections provide the find_one() and find() methods:
# 
# - The find_one() method selects and returns a single document from a collection and returns that document (or None if there are no matches). It is useful when you know there is only one matching document, or are only interested in the first match:

# <codecell>

posts.find_one()

# <markdowncell>

# - To get more than a single document as the result of a query we use the find() method. find() returns a Cursor instance, which allows us to iterate over all matching documents. 

# <markdowncell>

# posts.find()

# <markdowncell>

# For example, we can iterate over the first 2 documents (there are a lot in the collection and this is just an example) in the posts collection:

# <codecell>

for d in posts.find()[:2]:
    print d
    

# <markdowncell>

# you can also use the standard python list():

# <codecell>

list(posts.find())[:2]

# <markdowncell>

# ## Counting
# 
# If we just want to know how many documents match a query we can perform a count() operation instead of a full query. We can get a count of all of the documents in a collection:

# <codecell>

posts.count()

# <codecell>

posts.find().count()

# <markdowncell>

# ## Query Operators
# 
# MongoDB queries are represented as JSON-like structure, just like documents. To build a query, you just need to specify a dictionary with the properties you wish the results to match. For example, this query will match all documents in the posts collection with ISO language code "en".

# <codecell>

posts.find({"iso_language_code": "en"}).count()

# <markdowncell>

# If we wanted to retrieve all documents with ISO language code "en" and source equal to "twitterfeed":

# <codecell>

posts.find({"iso_language_code":"en","source":"twitterfeed"}).count()

# <markdowncell>

# Queries can also use special query operators. These operators include **gt, gte, lt, lte, ne, nin, regex, exists, not, or**, and many more. The following queries show the use of some of these operators.

# <codecell>

from datetime import datetime
# cheat: year, month, day, hour, minute, second, microsecond
date1 = datetime.strptime("18/01/13 18:30", "%d/%m/%y %H:%M")
date2 = datetime.strptime("18/01/13 18:05", "%d/%m/%y %H:%M")
date3 = datetime.strptime("18/01/13 18:10", "%d/%m/%y %H:%M")
date4 = datetime.strptime("18/01/13 18:25", "%d/%m/%y %H:%M")

cursor = posts.find({'created_at':{"$gt":date1}})
cursor.next()

# <markdowncell>

# This time we will do the same query but add the count() method to only get the count of documents that match the query. We will use count() from now onwards (easier!!!)

# <codecell>

posts.find({'created_at':{"$gt":date1}}).count()

# <codecell>

# Tweets dates low than or equal to date2
posts.find({'created_at':{"$lte":date2}}).count()

# <codecell>

# Between 2 dates
posts.find({"created_at": {"$gte": date3, "$lt": date4}}).count()

# <codecell>

# Posts in either spanish or french
posts.find({"iso_language_code":{"$in":["es","fr"]}}).count()

# <codecell>

# Posts in either spanish or french using $or
posts.find({"$or":[{"iso_language_code":"es"},{"iso_language_code":"fr"}]}).count()

# <codecell>

# All posts except spanish or french
posts.find({"iso_language_code":{"$nin":["es","fr"]}}).count()

# <codecell>

# Using Regex to find a post with hashtag #analytics
import re
regex = re.compile(r'#analytics')
rstats = posts.find_one({"text":regex})
rstats

# <markdowncell>

# We'll cover other operators further down once we have covered the Update process.
# 
# ## Sorting Documents
# 
# MongoDB can sort query results for you on the server-side. Especially if you are sorting results on a property which has an index, it can sort these far more efficiently than your client program can.
# 
# Here's an exmaple of using a descending sort to get the last tweet in our collection.

# <codecell>

lastTweet = posts.find().sort([("created_at", pymongo.DESCENDING)])
lastTweet.next()

# <markdowncell>

# What about the first tweet in french?

# <codecell>

frlastTweet = posts.find({"iso_language_code":"fr"}).sort([("created_at", pymongo.ASCENDING)])
frlastTweet.next()

# <markdowncell>

# The above queries are not very optimal when you have large result sets. Pymongo have a limit() method which let you fetch a limited number of results.

# <codecell>

lastTweetOnly = posts.find().sort([("created_at", pymongo.DESCENDING)]).limit(1)
for t in lastTweetOnly: print t

# <markdowncell>

# ## Updating Documents
# 
# PyMongo can update documents in a number of different ways. Let's start for adding a new document to our collection.

# <codecell>

posts.insert({"_id":1234,"created_at":datetime(2013,1,21,15,27,59),"text":"Hello World", "from_user":"Altons","source":"Ipython"})

# <codecell>

posts.find_one({"_id":1234})

# <markdowncell>

# Now we can use the update() method to modify the document. This operation finds the document we just inserted by _id and updates it with a new document.

# <codecell>

posts.update({"_id":1234},{"from_user":"anonymous"})

#Fetch our updated document
posts.find_one({"_id":1234})

# <markdowncell>

# The update() method replaces the whole document so be careful! If instead we want to modify specific fields of the document we can use MongoDB's update operators like **set, inc, push, pull** and many more.
# 
# ### Update Operator: set
# 
# This statement updates in the document in collection where field matches value1 by replacing the value of the field field1 with value2. This operator will add the specified field or fields if they do not exist in this document or replace the existing value of the specified field(s) if they already exist.

# <codecell>

posts.update({"_id":1234},{"$set":{"from_user":"Altons","source":"Ipython notebook"}})
posts.find_one({"_id":1234})

# <markdowncell>

# **Upsert**
# 
# An **upsert** eliminates the need to perform a separate database call to check for the existence of a record before performing either an update or an insert operation. Typically update operations update existing documents, but in MongoDB, the update() operation can accept an **upsert** option as an argument. Upserts are a hybrid operation that use the **query** argument to determine the write operation:
# 
# - If the query matches an existing document(s), the upsert performs an update.
# - If the query matches no document in the collection, the upsert inserts a single document.
# 
# Let's see an example:

# <codecell>

posts.update({"_id":5678},{"$set":{"from_user":"Alberto","source":"unavailable"}})
posts.find({"_id":5678}).count()

# <markdowncell>

# The update fails because no document matched the query for the update. But using upsert will sort this out:

# <codecell>

posts.update({"_id":5678},{"$set":{"from_user":"Alberto","source":"unavailable"}}, upsert=True)
posts.find({"_id":5678}).count()

# <markdowncell>

# **multi=True**
# 
# By default MongoDB only modifies the first document that matches the query. If you want to modify all documents that match the query add multi=True.

# <markdowncell>

# ### Update Operator: inc
# 
# The inc operator increments a value by a specified amount if field is present in the document. If the field does not exist, $inc sets field to the number value. For example:

# <codecell>

posts.update({"_id":1234},{"$set":{"total_posts":1}})
posts.find_one({"_id":1234})

# <codecell>

# Increment total_posts by 9 tweets
posts.update({"_id":1234},{"$inc":{"total_posts":9}})
posts.find_one({"_id":1234})

# <markdowncell>

# ###Update Operator: unset
# 
# The unset operator deletes a particular field. If documents match the initial query but do not have the field specified in the unset operation, there the statement has no effect on the document.
# 

# <codecell>

posts.update({"_id":1234},{"$unset":{"total_posts":""}})
posts.find_one({"_id":1234})

# <markdowncell>

# ### Update Operator: rename
# 
# The rename operator updates the name of a field. The new field name must differ from the existing field name.

# <codecell>

posts.update({"_id":1234},{"$rename":{"from_user":"username"}})
posts.find_one({"_id":1234})

# <markdowncell>

# Here we have a good opportunity to see **exists** in action (it should return only 1 as there only one document with field **username**):

# <codecell>

posts.find({"username":{"$exists":True}}).count()

# <markdowncell>

# ### Update Operator: push 
# 
# The **push** operator appends a specified value to an array.Be aware of the following behaviors:
# 
# - If the field specified in the **push** statement (e.g. { $push: { field: value1 } }) does not exist in the matched document, the operation adds a new array with the specified field and value (e.g. value1) to the matched document.
# - The operation will fail if the field specified in the **push** statement is not an array. $push does not fail when pushing a value to a non-existent field.
# - If value1 is an array itself, **push** appends the whole array as an element in the identified array. To add multiple items to an array, use [pushAll](http://docs.mongodb.org/manual/reference/operator/pushAll/#_S_pushAll).
# 
# Now for this example, let's say we have 2 predictive models that score the sentiment of each tweet in the range -5,5 (-5 = worse, 0 = neutral and 5=best) and we want to add those scores to each document.
# 
# Let's use our well known document _id=1234

# <codecell>

import random

posts.update({"_id":1234},{"$push":{"sentiment":{"nb":random.randint(-5, 5),"svm":random.randint(-5, 5)}}})
posts.find_one({"_id":1234})

# <markdowncell>

# In the above example we have added scores to document 1234, let's see what happens if we run the same code again.

# <codecell>

posts.update({"_id":1234},{"$push":{"sentiment":{"nb":random.randint(-5, 5),"svm":random.randint(-5, 5)}}})
posts.find_one({"_id":1234})

# <markdowncell>

# it will add another array as expected. I don't know why one would think it will update the original array instead of appending a new one. So don't make the mistake I did!
# 
# if you run it twice or more you always have the **unset** operator to the rescue (if you want to start from scratch!)

# <codecell>

posts.update({"_id":1234},{"$unset":{"sentiment":""}})
posts.find_one({"_id":1234})

# <markdowncell>

# ### Update Operator: pop
# 
# The **pop** operator removes the first or last element of an array. Pass **pop** a value of 1 to remove the last element in an array and a value of -1 to remove the first element of an array.
# 
# Be aware of the following **pop** behaviors:
# 
# - The **pop** operation fails if field is not an array.
# - **pop** will successfully remove the last item in an array. field will then hold an empty array.
# 
# We can use **pop** if we don't want to start (or can't) from scratch:

# <codecell>

posts.update({"_id":1234},{"$push":{"sentiment":{"nb":random.randint(-5, 5),"svm":random.randint(-5, 5)}}})
posts.update({"_id":1234},{"$push":{"sentiment":{"nb":random.randint(-5, 5),"svm":random.randint(-5, 5)}}})
posts.find_one({"_id":1234})

# <codecell>

posts.update({"_id":1234},{"$pop":{"sentiment":1}})
posts.find_one({"_id":1234})

# <markdowncell>

# ### Update Operator: pull
# 
# The **pull** operator removes all instances of a value from an existing array. If the value existed multiple times in the field array, **pull** would remove all instances of this value in this array.
# 
# It is very handy when you exactly what value you want to remove.

# <codecell>

posts.update({"_id":5678},{"$set":{"skills":["python","SAS","R","javascript","java"]}})
posts.find_one({"_id":5678})

# <codecell>

posts.update({"_id":5678},{"$pull":{"skills":"java"}})
posts.find_one({"_id":5678})

# <markdowncell>

# ### Update Operator: addToSet
# 
# The **addToSet** operator adds a value to an array only if the value is not in the array already. If the value is in the array, **addToSet** returns without modifying the array. Otherwise, **addToSet** behaves the same as **push**

# <codecell>

posts.find_one({"_id":5678})

# <codecell>

posts.update({"_id":5678},{"$addToSet":{"skills":"python"}})
posts.find_one({"_id":5678})

# <codecell>

posts.update({"_id":5678},{"$addToSet":{"skills":"Perl"}})
posts.find_one({"_id":5678})

# <markdowncell>

# ###Update Operator: $
# 
# The positional $ operator identifies an element in an array field to update without explicitly specifying the position of the element in the array. The positional operator, when used with the update() method and acts as a placeholder for the first match of the update query selector.

# <codecell>

# sample document
posts.update({"_id":1234},{"$set":{"skills":["python","SAS","R","javascript","java"]}})
posts.find_one({"_id":1234})

# <codecell>

# update R to Rstats
posts.update({"_id":1234,"skills":"R"},{ "$set": { "skills.$" : "Rstats" }})
posts.find_one({"_id":1234})

# <codecell>

# Another example
posts.update({"_id":1234},{"$push":{"sentiment":{"nb":random.randint(-5, 5),"svm":random.randint(-5, 5)}}})
posts.find_one({"_id":1234})

# <codecell>

# Use the positional $ operator to update the value of the nb field to zero in the embedded document with the svm of 4:
posts.update({"_id":1234,"sentiment.svm":4},{ "$set": { "sentiment.$.nb" : 0 }})
posts.find_one({"_id":1234})

# <markdowncell>

# ## Removing Data
# 
# Removing databases, collections and documents in Pymongo is a straight forward process:

# <codecell>

conn.database_names()

# <codecell>

# Remove database sandpit-test
conn.drop_database("sandpit-test")
conn.database_names()

# <codecell>

# Create a database, then a collection and a dummy document
conn.dummy.dummy_collection.insert({"greeting":"Hello World"})
conn.dummy.collection_names()

# <codecell>

conn.dummy.collection_names()

# <codecell>

# Delete a collection
conn.dummy.drop_collection("dummy_collection")
conn.dummy.collection_names()

# <codecell>

# Delete dummy database
conn.drop_database("dummy")
conn.database_names()

# <codecell>

# Remove documents.
#  Please note that there is no multi=True option for remove. MongoDB will remove any documents that match the query
posts.remove({"_id":5678})

# <markdowncell>

# If we don't specify what documents to remove MongoDB will remove them all. This just removes the documents. The collection and its indexes still exist.

# <markdowncell>

# ## Useful Commands
# 
# If you need to get some statistics about your collections.

# <codecell>

db.command({'dbstats': 1})

# <markdowncell>

# To get collection statistics use the collstats command:

# <codecell>

db.command({'collstats': 'posts'})

# <markdowncell>

# ## Things I did not covered in this tutorial
# 
# - [Aggregation Framework](http://docs.mongodb.org/manual/reference/aggregation/) (Still chinese to me).
# - [Map Reduce](http://docs.mongodb.org/manual/applications/map-reduce/)
# - [GridFS](http://docs.mongodb.org/manual/applications/gridfs/)
# - [Journaling](http://docs.mongodb.org/manual/administration/journaling/) 

# <markdowncell>

# I hope you find this tutorial useful. I'll be using it as my online cheat sheet! 

