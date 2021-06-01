import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from random import shuffle

def get_data():
    tourd=pd.read_excel("dataset/data-ver-2.xlsx",index_col=0)
    tourd['category']=tourd['category'].fillna('')
    return tourd

def transform_data(data):
    count = CountVectorizer(stop_words='english')
    count_matrix1 = count.fit_transform(data['category'])
    count_matrix2 = count.fit_transform(data['state'])
    
    combine_sparse = sp.hstack([count_matrix1,count_matrix2], format='csr')
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
    
    return cosine_sim

def recommend_destinations(title, data, transform):
    indices = pd.Series(data.index, index = data['name'])
    
    index = indices[title]
    sim_scores = list(transform[index])
    for i in range(len(sim_scores)):
      sim_scores[i]=[i,sim_scores[i]]
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:81]


    for i in range(len(sim_scores)):
      sim_scores[i][1] = sim_scores[i][1] * data['rating'].iloc[sim_scores[i][0]] * data['numberOfRating'].iloc[sim_scores[i][0]]

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    dest_indices = [i[0] for i in sim_scores]

    dest_state = data['address'].iloc[dest_indices]
    dest_name = data['name'].iloc[dest_indices]
    dest_desc = data['big_description'].iloc[dest_indices]

    recommendation_data = pd.DataFrame(columns=['name','address', 'description'])

    recommendation_data['address'] = dest_state
    recommendation_data['name'] = dest_name
    recommendation_data['description'] = dest_desc

    return recommendation_data

def results(destination):
    data = get_data()

    df = {'name':'curr_user','category':category_dictionary[category],'popularity':'','ratingClass':'','state':''	}
    data=data.append(df,ignore_index=True)
        
    transform_result = transform_data(data)

    recommendations = recommend_destinations("curr_user", data, transform_result)
    return recommendations.to_dict('records')

def combine_results(cat_list):
  cat_list=list(cat_list.split(","))
  noe=20//len(cat_list)
  finalrec=[]
  for i in cat_list:
    rec=results(i)
    if len(cat_list)>1:
      rec=rec[0:10]
    shuffle(rec)
    j,k=0,0
    while j<noe:
      if rec[k] not in finalrec: 
        finalrec.append(rec[k])
        k+=1
        j+=1
      else:
        k+=1
  return finalrec

