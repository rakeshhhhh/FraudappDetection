import pandas as pd
import numpy as np
import pickle

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score

#import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')




class AppClassification:

    def __init__(self):
        pass

    ########## ALGORITHM #############
    def naive_bayes_model(self,Train_X_Tfidf, Train_Y, Test_X_Tfidf,Test_Y):
        print("Classifier - Algorithm - Naive Bayes")
        Naive = naive_bayes.MultinomialNB()
        Naive.fit(Train_X_Tfidf, Train_Y)
        predictions_NB = Naive.predict(Test_X_Tfidf)
        print("Naive Bayes Accuracy Score -> ", accuracy_score(predictions_NB, Test_Y) * 100)
        return Naive

    def svm_model(self,Train_X_Tfidf, Train_Y,Test_X_Tfidf,Test_Y):
        print("Classifier - Algorithm - SVM")
        SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        SVM.fit(Train_X_Tfidf, Train_Y)
        predictions_SVM = SVM.predict(Test_X_Tfidf)
        print("SVM Accuracy Score -> ", accuracy_score(predictions_SVM, Test_Y) * 100)
        return SVM

    def save_data(self,fname, classifier):
        with open(fname, 'wb') as picklefile:
            pickle.dump(classifier, picklefile)

    def load_data(self,fname):
        with open(fname, 'rb') as training_model:
            model = pickle.load(training_model)
        return model


    def get_prediction(self,model,Corpus,Tfidf_vect):
        Test_X = Corpus['text_final']
        Test_X_Tfidf = Tfidf_vect.transform(Test_X)
        predictions_NB = model.predict(Test_X_Tfidf.toarray())
        print(predictions_NB)
        return predictions_NB
    #######################

    def text_processing(self,csvfile,labelfile):
        np.random.seed(500)
        Corpus = pd.read_csv(csvfile,encoding='latin-1')
        print(Corpus['label'].unique())
        self.save_data(labelfile,Corpus['label'].unique())
        Corpus['text'].dropna(inplace=True)
        Corpus['text'] = [entry.lower() for entry in Corpus['text']]
        Corpus['text']= [word_tokenize(entry) for entry in Corpus['text']]
        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
        for index,entry in enumerate(Corpus['text']):
            Final_words = []
            word_Lemmatized = WordNetLemmatizer()
            for word, tag in pos_tag(entry):
                if word not in stopwords.words('english') and word.isalpha():
                    word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                    Final_words.append(word_Final)
            Corpus.loc[index,'text_final'] = str(Final_words)
        print(Corpus['text_final'].head())
        return Corpus

    def input_text_processing(self,csvcontent):
        data = [['label', csvcontent]]
        Corpus =pd.DataFrame(data, columns=['label', 'text'])
        print(Corpus['label'].unique())
        Corpus['text'].dropna(inplace=True)
        Corpus['text'] = [entry.lower() for entry in Corpus['text']]
        Corpus['text']= [word_tokenize(entry) for entry in Corpus['text']]
        tag_map = defaultdict(lambda : wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
        for index,entry in enumerate(Corpus['text']):
            Final_words = []
            word_Lemmatized = WordNetLemmatizer()
            for word, tag in pos_tag(entry):
                if word not in stopwords.words('english') and word.isalpha():
                    word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                    Final_words.append(word_Final)
            Corpus.loc[index,'text_final'] = str(Final_words)
        print(Corpus['text_final'].head())
        return Corpus


    def train_model(self,Corpus,tfidfile,modelfile,algo):
        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Corpus['text_final'],Corpus['label'],test_size=0.3)
        Encoder = LabelEncoder()
        Train_Y = Encoder.fit_transform(Train_Y)
        Test_Y = Encoder.fit_transform(Test_Y)
        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(Corpus['text_final'])
        Train_X_Tfidf = Tfidf_vect.transform(Train_X)
        Test_X_Tfidf = Tfidf_vect.transform(Test_X)

        self.save_data(tfidfile,Tfidf_vect)
        if (algo == 'svm'):
            SVM = self.svm_model(Train_X_Tfidf, Train_Y,Test_X_Tfidf,Test_Y)
            self.save_data(modelfile,SVM)
        elif(algo=='naive_bayes'):
            Naive = self.naive_bayes_model(Train_X_Tfidf, Train_Y, Test_X_Tfidf,Test_Y)
            self.save_data(modelfile, Naive)
        print("DONE")

def main():

    obj = AppClassification()
    #txt_result = obj.text_processing(r"c_small.csv",r'c_small_label.dat')
    #obj.train_model(txt_result,r'c_small_tfid.dat',r'c_small_svm.model','svm')

    #msg = "Stuning even for the non-gamer: This sound track was beautiful! It paints the senery in your mind so well I would recomend it even to people who hate video game music! I have played the game Chrono Cross but out of all of the games I have ever played it has the best music! It backs away from crude keyboarding and takes a fresher step with grate guitars and soulful orchestras. It would impress anyone who cares to listen! ^_^"
    #result = obj.input_text_processing(msg)
    #model = obj.load_data('c_small_svm.model')
    #Tfidf_vect = obj.load_data('c_small_tfid.dat')
    #p = obj.get_prediction(model, result, Tfidf_vect)
    #label = obj.load_data(r'c_small_label.dat')
    #print(f'result = {label[p[0]]}')

if __name__ == '__main__':
    main()