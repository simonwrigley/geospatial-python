import wikipedia
​
# Summary paragraph
print(wikipedia.WikipediaPage(title = 'Article Title').summary)
​
# List of image URLS
print(wikipedia.WikipediaPage(title = 'Article Title').images)
​
# Lat/Lon coordiantes of the object.
print(wikipedia.WikipediaPage(title='Article Title').coordinates)

# Lat/Lon coordiantes of the object.
print(wikipedia.WikipediaPage(title = 'Article Title').coordinates)
​
