import re, math, collections, itertools, os, sys, pickle
import nltk
import nltk.classify.util
import nltk.metrics
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import precision, recall
from nltk.probability import FreqDist, ConditionalFreqDist

DATA_DIR = os.path.join('data', 'rt-polaritydata')
RT_POS_FILE = os.path.join(DATA_DIR, 'rt-polarity-pos.txt')
RT_NEG_FILE = os.path.join(DATA_DIR, 'rt-polarity-neg.txt')
NAIVEBAYES_CLASS_FILE = os.path.join('data', 'naive_bayes_classifier.pickle')

#this function takes a feature selection mechanism and returns its performance in a variety of metrics
def train_set():
    print "Training data set and dumping to pickle file ./data/naive_bayes_classifier.pickle"

    posFeatures = []
    negFeatures = []

    #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
    train_pos = []
    train_neg = []
    with open(RT_POS_FILE, 'r') as posSentences:
        for i in posSentences:
            train_pos.append((i, 'pos'))

        all_words = set(word.lower() for passage in train_pos for word in word_tokenize(passage[0]))
        print "Extracted all positive words..."
        posFeatures = [[{word: (word in word_tokenize(x[0])) for word in all_words}, x[1]] for x in train_pos]
        print "Prepared positive word feature set..."
    with open(RT_NEG_FILE, 'r') as negSentences:
        for i in negSentences:
            train_neg.append((i, 'neg'))

        all_words = set(word.lower() for passage in train_neg for word in word_tokenize(passage[0]))
        print "Extracted all negative words..."
        negFeatures = [[{word: (word in word_tokenize(x[0])) for word in all_words}, x[1]] for x in train_neg]
        print "Prepared negative word feature set..."

    trainFeatures = posFeatures[:] + negFeatures[:]

    #trains a Naive Bayes Classifier
    classifier = NaiveBayesClassifier.train(trainFeatures)
    #Dump the classifier to a pickle file
    naive_bayes_classifier_file = open(NAIVEBAYES_CLASS_FILE, 'wb')
    pickle.dump(classifier, naive_bayes_classifier_file)
    naive_bayes_classifier_file.close()

    # Retrain the feature set for analysis:
    # Determine the precision and recall
    trainFeatures = []
    testFeatures = []
    posCutoff = int(math.floor(len(posFeatures)*3/4))
    negCutoff = int(math.floor(len(negFeatures)*3/4))
    trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
    testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]

    #initiates referenceSets and testSets
    referenceSets = collections.defaultdict(set)
    testSets = collections.defaultdict(set)

    # Train classifier again
    test_classifier = NaiveBayesClassifier.train(trainFeatures)

    #puts correctly labeled sentences in referenceSets and the predictively labeled version in testsets
    for i, (features, label) in enumerate(testFeatures):
        referenceSets[label].add(i)
	predicted = test_classifier.classify(features)
	testSets[predicted].add(i)

    #prints metrics to show how well the feature selection did
    print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
    print 'accuracy:', nltk.classify.util.accuracy(test_classifier, testFeatures)
    print 'pos precision:', precision(referenceSets['pos'], testSets['pos'])
    print 'pos recall:', recall(referenceSets['pos'], testSets['pos'])
    print 'neg precision:', precision(referenceSets['neg'], testSets['neg'])
    print 'neg recall:', recall(referenceSets['neg'], testSets['neg'])

    #prints metrics to show how well the feature selection did
    classifier.show_most_informative_features(10)

if __name__ == "__main__":
    train_set()
