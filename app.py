from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
products = pickle.load(open('products.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           Product_Name=list(popular_df['Furniture-Type'].values),
                           Product_brand=list(popular_df['Furniture-Brand'].values),
                           Product_Image=list(popular_df['Image-Url'].values),
                           Votes=list(popular_df['num_rating'].values),
                           Ratings=list(popular_df['avg_rating'].values),
                           Price=list(popular_df['Furniture-Price'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_products', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:9]

    data = []
    for i in similar_items:
        item = []
        temp_df = products[products['Furniture-Type'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Furniture-Type')['Furniture-Type'].values))
        item.extend(list(temp_df.drop_duplicates('Furniture-Type')['Furniture-Brand'].values))
        item.extend(list(temp_df.drop_duplicates('Furniture-Type')['Furniture-Price'].values))
        item.extend(list(temp_df.drop_duplicates('Furniture-Type')['Image-Url']))
        data.append(item)

        print(data)
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
