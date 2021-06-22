import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix


movies=pd.read_csv("movies.csv")
ratings=pd.read_csv('final.csv')

user_rating_conne = ratings.pivot_table(index=['movieId'],columns=['userId'],values='New_score')
user_rating_conne = user_rating_conne.fillna(0,axis=1)
rating_csr_matrix=csr_matrix(user_rating_conne.values)

model=NearestNeighbors(metric="cosine",n_neighbors=20,radius=1)
model.fit(rating_csr_matrix)

data=list(user_rating_conne.index)

def inputid(mid):

    query_index=data.index(mid)
    similarity,indices=model.kneighbors(user_rating_conne.iloc[query_index,:].values.reshape(1,-1))

    recommendations=[]
    recommendations.append(movies[movies.movieId==mid]['title'].values[0])

    for i in range(1,10):
        mid=indices[0][i]
        if(mid not in data):
            None
        else:
            recommendations.append(movies[movies.movieId==mid]['title'].values[0])


    str1="\n"
    return (str1.join(recommendations))




