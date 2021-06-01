import pandas as pd
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_data():
    tourd=pd.read_excel("dataset/final_states.xlsx",index_col=0)
    tourd=tourd.dropna()
    return tourd

def transform_data(data):
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(data['description'])

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['description'])

    combine_sparse = sp.hstack([count_matrix,tfidf_matrix], format='csr')
    cosine_sim = cosine_similarity(combine_sparse, combine_sparse)
        
    return cosine_sim

def recommend_destinations(title, data, transform):
    indices = pd.Series(data.index, index = data['name'])
    index = indices[title]



    sim_scores = list(enumerate(transform[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]


    dest_indices = [i[0] for i in sim_scores]

    dest_state = data['state'].iloc[dest_indices]
    dest_name = data['name'].iloc[dest_indices]
    dest_desc = data['description'].iloc[dest_indices]

    recommendation_data = pd.DataFrame(columns=['state','name', 'description'])

    recommendation_data['state'] = dest_state
    recommendation_data['name'] = dest_name
    recommendation_data['description'] = dest_desc

    return recommendation_data

def results(destination):
    data = get_data()
    transform_result = transform_data(data)

    if destination not in data['name'].unique():
        return 'Destination not in Database'

    else:
        recommendations = recommend_destinations(destination, data, transform_result)
        return recommendations.to_dict('records')

