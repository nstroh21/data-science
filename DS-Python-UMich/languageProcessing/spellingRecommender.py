from nltk.corpus import words

nltk.download('words')
correct_spellings = words.words()
correct_spellings[0:20]

#Jaccard Distance
#The Jaccard coefficient measures similarity between finite sample sets, and is defined as the size of the intersection divided by the size of the union of the sample sets:
# the directions also do say to search only the words that start with the same letter, assume a person is likely to get at least the first letter right
#re is in fact a more efficient way, my code is checking jaccard distnace on every individual n-gram 
# but I want to becreating the ngrams and then taking the overall jaccard distance on the set of ngrams (not each individual gram)

from nltk.util import ngrams
from nltk.metrics.distance import jaccard_distance, edit_distance

def answer_nine(entries=['cormulent', 'incendenece', 'validrate']):
    
    recommend = []
    
    for word in entries:
        
        rec_list = []  # place holder list which will contain every word in dictionary looped through
        j_list = [] # placeholder list which will contain the corresponding jaccard scores
        
        first_letter = word[0]
        correct_spellings1 = [w for w in correct_spellings if w.startswith(first_letter) == True and len(w) >= 3]
                
        for test in correct_spellings1:
            
            # since this is counting empty sets as 1 when it takes jaccard, just have to do it manually instead
            #ngram_jaccard = jaccard_distance( set(ngrams(test, 3)), set(ngrams(word,3)) )
            
            test_set = set(ngrams(test, 3))
            word_set = set(ngrams(word,3)) 
            
            inter = len(test_set.intersection(word_set))
            union = len(test_set.union(word_set))
            
            j = inter/ union
            
            j_list.append(j)
            rec_list.append(test)
        
        rec_index = np.argmax(j_list)
        rec = rec_list[rec_index]
        
        recommend.append(rec)
                      
    return recommend
answer_nine()


#Jaccard Distance on 4-grams
def answer_ten(entries=['cormulent', 'incendenece', 'validrate']):
    
    recommend = []
    
    # step through trigrams for each word  (double for loop gotta wonder if there are more efficient ways)
    for word in entries:
        
        rec_list = []  # place holder list which will contain every word in dictionary looped through
        j_list = [] # placeholder list which will contain the corresponding jaccard scores
        
        first_letter = word[0]
        correct_spellings1 = [w for w in correct_spellings if w.startswith(first_letter) == True and len(w) >= 3]
                
        for test in correct_spellings1:
            
            # since this is counting empty sets as 1 when it takes jaccard, just have to do it manually instead
            #ngram_jaccard = jaccard_distance( set(ngrams(test, 3)), set(ngrams(word,3)) )
            
            test_set = set(ngrams(test, 4))
            word_set = set(ngrams(word, 4)) 
            
            inter = len(test_set.intersection(word_set))
            union = len(test_set.union(word_set))
            
            j = inter/ union
            
            j_list.append(j)
            rec_list.append(test)
        
        rec_index = np.argmax(j_list)
        rec = rec_list[rec_index]
        
        recommend.append(rec)
        
    return recommend
        
answer_ten()



#edit distance method
# use the nltk built-in edit_distance for this problem
from nltk.metrics.distance import jaccard_distance, edit_distance

def answer_eleven(entries=['cormulent', 'incendenece', 'validrate']):
    
    recommend = [] 
        
    for word in entries:  
        
        first_letter = word[0]
        correct_spellings1 = [w for w in correct_spellings if w.startswith(first_letter) == True and len(w) >= 3]
        
        rec_list = []  # place holder list which will contain every word in dictionary looped through
        dist_list = [] # placeholder list which will contain the corresponding jaccard scores
        
        for test in correct_spellings1:
            dist = edit_distance(word, test)
            rec_list.append(test)
            dist_list.append(dist)
        
        rec_index = np.argmin(dist_list)
        rec = rec_list[rec_index]
        
        recommend.append(rec)   
   
    return recommend
    
answer_eleven()