Hey.
I'm writing a short text to explain what I wanted to do in this short project:
Because we are handling text, the classic thing is to clean it.
I used several techniques (all are configurable):
1. remove punct
2. remove digits
3. stem
4. remove stop words
5. lower()

After that I wanted to pick the words that actually matter
so I used tf idf in order to drop common words.

When I finished I got shorter strings (we can only search
len of 50 strings at alibaba), most of them are less
then 50 chars (not all of them - I decided to move on).

Then I took the new texts that represent the amazon items
and searched for them at alibaba.

Then again - I did the same cleaning process to the alibaba
results.

At the end of this process I moved towards scoring the search
results.
At this point I wrote a naive solution in which im counting
how many exact matches in terms of single words each search
result have (compared to the amazon item clean text).

I sorted this score and thats it.
I also calculated the percent of the amazon item words that
are in each one of the alibaba items text in order to try and
get a better understanding of the match quality


Things I planned and additional options in bullets:
1. auto detect stop words (common words in the text from amazon)
2. Use other fields and not just the title. I did clean some
more fields from amazon like categories
3. Extract the 'main idea' of a text using some kind of a model
like LDA.
For example - this link
https://towardsdatascience.com/nlp-extracting-the-main-topics-from-your-dataset-using-lda-in-minutes-21486f5aa925

4. After searching alibaba - transform the results and the
amazon item texts to vector - tf_idf vectorizer, word2vec, 
doc2vec... and maybe other vectorizing methods - then calc
the distance between the vectors.

5. Multi processing for cleanning the texts, searching alibaba, ETC
 
 
