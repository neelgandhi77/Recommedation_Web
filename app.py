from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///datas.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class toentry(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    Recommended_Movies=db.Column(db.String(500),nullable=False)
    timestamp=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr(self) -> str:
        return f"{self.sno} - {self.Recommended_Movies}"





movies=pd.read_csv("movies.csv")
ratings=pd.read_csv("final.csv")

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


    #str1=", "
    return (recommendations)

@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        toentry.query.delete()
        id=request.form["name"]
        answer=inputid(int(id))
        for i in answer:
            obj=toentry(Recommended_Movies=i)
            db.session.add(obj)
            db.session.commit()
    allR=toentry.query.all()

    answer=""
    return render_template('index.html',allR=allR)


@app.route("/show")
def show_screen():
    allR=toentry.query.all()
    #print(allR)



if __name__=="__main__":
    app.run(debug=True)