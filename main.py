from edmga_trainer import utils
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--track', help='spotifyの楽曲へのリンク')
    parser.add_argument('-v', '--validate', action='store_true', help='テストデータを検証します')
    args = parser.parse_args()
    
    data_loader = utils.DataLoader()
    mm = MinMaxScaler()
    min_max_data = mm.fit_transform(data_loader.data)
    
    x_train, x_test, y_train, y_test = train_test_split(
        min_max_data, data_loader.target, test_size=0.2, random_state=0
    )
    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)
    
    if (args.validate):
        y_pred = model.predict_proba(x_test)
        print(x_test)
        print("Top3 score: " + str(metrics.top_k_accuracy_score(y_test, y_pred, k=3)))
    if args.track is not None:
        print("楽曲を解析します")
        id = args.track.split('/')[4]
        utils.get_spotify_token()
        utils.set_token_to_headers()
        x = utils.get_spotify_features(id)
        x = np.array(x).reshape(1, -1)
        data_loader.data[0] = x
        x = mm.fit_transform(data_loader.data)[0].reshape(1,-1)
        y = model.predict_proba(x)[0]
        print_top_k(y)

def print_top_k(y, k=3):
    index = np.argsort(y)[::-1]
    for i in range(k):
        genre = utils.genres_list[index[i]]
        pred = y[index[i]] * 100
        print(f"{i+1}: {genre}", '{:.2f}'.format(pred), "%")
    
if __name__ == '__main__':
    main()
