from edmga_trainer import utils
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def main():
    data_loader = utils.DataLoader()
    mm = MinMaxScaler()
    min_max_data = mm.fit_transform(data_loader.data)
    
    x_train, x_test, y_train, y_test = train_test_split(
        min_max_data, data_loader.target, test_size=0.2, random_state=0
    )
    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)
    
    y_pred = model.predict_proba(x_test)
    
    print("Top3 score: " + str(metrics.top_k_accuracy_score(y_test, y_pred, k=3)))
    
if __name__ == '__main__':
    main()
