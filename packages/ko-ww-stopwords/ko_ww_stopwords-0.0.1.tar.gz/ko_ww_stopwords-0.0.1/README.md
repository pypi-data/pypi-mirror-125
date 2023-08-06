# ko-ww-stopwords
This is a set of whole-word (independent) stop words in Korean. Dependent stop words, on the other hand, are difficult to identify without using a part-of-speech tagger, but it is easy to identify whole-word (independent) stop words.

## Code Sample

from ko_ww_stopwords.stop_words import ko_ww_stop_words
from ko_ww_stopwords.tools import is_stop_word, strip_outer_punct

print(ko_ww_stop_words)

#is_stop_word(word)
#Returns true if word is a whole-word stop word.

print("우선 is_stop_word -> {}".format(is_stop_word("우선")))

print("서울 is_stop_word -> {}".format(is_stop_word("서울")))

#strip_outer_punct(word)
#Strips leading and trailing punctuation marks from word.

raw_str = "(우선)"

print("raw_str is_stop_word -> {}".format(is_stop_word(raw_str)))

normalized_str = strip_outer_punct(raw_str)

print("normalized_str is_stop_word -> {}".format(is_stop_word(normalized_str)))


## Other Packages

If you need a Korean sentence tokenizer, please see https://github.com/Rairye/kr-sentence