from flask import Flask, request, render_template
import pandas as pd
import random

from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel


app = Flask(__name__)


#load_files

trending_products = pd.read_csv("C:/Users/Latonya Smith/OneDrive/Desktop/Proj1folder/models/trending_products.csv")
train_data = pd.read_csv("C:/Users/Latonya Smith/OneDrive/Desktop/Proj1folder/models/clean_data.csv")


# database configuration

#app.secret_key = "kvivhdsvcuvaelbzdcvaedmkfbsivaebba"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@127.0.0.1/ecom"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#model calss for SignUp
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password= db.Column(db.String(100), nullable = False)


class Signin(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

def truncate(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def content_based_recommendations(train_data, item_name, top_n):
    #check if item name in training_data
    if item_name not in train_data['Name'].values:
        print("Item {} not found in the training data".format('item_name'))
        return pd.DataFrame()
    
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")

    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])

    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    item_index = train_data[train_data['Name']== item_name].index[0]
    similar_items = list(enumerate(cosine_similarities_content[item_index]))
    sort_rec_num_similar_items = sorted(similar_items, key= lambda x:x[1], reverse=True)

    top_similar_items = sort_rec_num_similar_items[1:top_n+1]


    recommended_items_indices = [x[0] for x in top_similar_items]

    recommended_items_details= train_data.iloc[recommended_items_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    return recommended_items_details                             
#routes

random_image_urls = [
    "static/img/img_1.png",
    "static/img/img_2.png",
    "static/img/img_3.png",
    "static/img/img_4.png",
    "static/img/img_5.png",
    "static/img/img_6.png",
    "static/img/img_7.png",
    "static/img/img_8.png",
]


#List of prices

@app.route("/")
def index():
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    prices = [40, 50, 150, 70, 100, 122, 106, 50, 30, 50]
    return render_template ('index.html', trending_products=trending_products.head(8), truncate = truncate,random_product_image_urls=random_product_image_urls, random_price = random.choice(prices))

@app.route("/main")
def main():
    empty_df = pd.DataFrame()
    return render_template('main.html', content_based_recs=empty_df)

@app.route("/index")
def indexredirect():
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    prices = [40, 50, 150, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products=trending_products.head(8), truncate = truncate,random_product_image_urls=random_product_image_urls, random_price = random.choice(prices))


@app.route("/signup", methods=['POST', 'GET'])

def signup():
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]

        prices = [40, 50, 150, 70, 100, 122, 106, 50, 30, 50]
        return render_template ('index.html', trending_products=trending_products.head(8), truncate = truncate,random_product_image_urls=random_product_image_urls, random_price = random.choice(prices), signup_message='User signed up successfully!')
    
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        username = request.form['signinUsername']
        password = request.form['signinPassword']
        new_signin = Signin(username=username, password=password)
        db.session.add(new_signin)
        db.session.commit()

        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        prices = [40, 50, 150, 70, 100, 122, 106, 50, 30, 50]
        return render_template ('index.html', trending_products=trending_products.head(8), truncate = truncate,random_product_image_urls= random_product_image_urls, random_price = random.choice(prices), signup_message='User signed in successfully!')



@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr'))
        content_based_recs = content_based_recommendations(train_data, prod, top_n=nbr)

        prices = [40, 50, 150, 70, 100, 122, 106, 50, 30, 50]

        if content_based_recs.empty:
            message = "No recommendations available for this product"
            # still pass an empty DataFrame so Jinja doesn't break
            return render_template(
                'main.html',
                message=message,
                content_based_recs=pd.DataFrame(),
                trending_products=trending_products.head(8),
                truncate=truncate,
                random_product_image_urls=[],
                random_price=random.choice(prices)
            )
        else:
            # create random image URLs for each recommended product
            random_product_image_urls = [
                random.choice(random_image_urls)
                for _ in range(len(content_based_recs))
            ]
            print(content_based_recs)
            print(random_product_image_urls)

            return render_template(
                'main.html',
                content_based_recs=content_based_recs,
                trending_products=trending_products.head(8),
                truncate=truncate,
                random_product_image_urls=random_product_image_urls,
                random_price=random.choice(prices)
            )

        
if __name__=='__main__':
    app.run(debug= True)

