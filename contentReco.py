import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import linear_kernel



ds = pd.read_csv("/Users/yanis/Downloads/eng-prods-swg (1).csv")
ds=ds.dropna(axis=0, how='any')
ds=ds.reset_index(drop=True,inplace=False)
ds['merge'] = ds.pro_loc_libelle.str.cat(ds.pro_loc_sousTitre,sep='. ')
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
'''the rows of the tfidf_matrix are the number of products 
the columns for each row are the number of occurences of each word'''

#I combined two columns
tfidf_matrix = tf.fit_transform(ds['merge'])


#this is the score
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)



rec_table = {}



for col, row in ds.iterrows():

    similar_indices = cosine_similarities[col].argsort()[:-20:-1]
    #we recommend up to 20 products(more than enough!!!)
    similar_items = [(cosine_similarities[col][i], ds['pro_id'][i]) for i in similar_indices]

    rec_table[row['pro_id']] = similar_items[1:]
    
    # we remove the first item because it is itself (it is why we begin [1:].
    #the result is a dictionary consisting of tuples:[(score,item_id),(score,item_id),...]
#print results[380][:5]

'''
If you want the most similar item_id to item3: results[3][:1][0][1].
explanation: [3] is item id
             [:1] we want one similar item_id ([:5] we want 5 similar items)
             [0][1] first row second column 
If we wanted the third most similar item_id to item3: results[3][:3][2][1].
'''

'''item(id) returns the name of the item without description when it is mixed thanks to the split(' - ')'''

def item(id):

    return ds.loc[ds['pro_id'] == id]['merge'].tolist()[0].split('   ')[0]
#useful if the item description is to long(stopping description)


def recommend(item_id, num):

        
    if num<=20:
        i=1

        print

        print("I will recommend using the cosine similarity score up to " + str(num) + " products similar to item_id " + str(item_id) + " :" + item(item_id) + ".")

        print

        recos = rec_table[item_id][:num]

        previous_rec=0

        for rec in recos:

        #to not display twice the same products

            if previous_rec!=rec[0]and rec[0]!=0:

                print("-Recommendation "+str(i)+ ":" + item(rec[1]) + " (the score is:" + str(rec[0]) + " and the item_id is:"+ str(rec[1])+").")

                i=i+1

                print

            previous_rec=rec[0]
    
    else:
        print ("We can only give you up to 20 similar products ! Please reduce the number of similar products")




recommend(item_id=420, num=2)

