from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from joblib import dump, load



# def predict_available_bike(Day, Hour, Station_number, Bike_stands, Banking, Bonus, main, temp, feels_like,temp_min, temp_max, wind_speed, pressure, humidity):
def save_models():
    integrated = pd.read_csv("Train_dataset_mar14_mar20.csv")
    train_feature = ["Day", "Hour", "Station_number", 'Bike_stands', 'Banking', 'Bonus', 'main', 'temp', 'feels_like'
        , 'temp_min', 'temp_max', 'wind_speed', 'pressure', 'humidity']
    target_feature1 = ['Available_bikes']
    target_feature2 = ['Available_bike_stands']

    train = integrated[train_feature]
    target = integrated[target_feature1]
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(train, target, test_size=0.3)

    Xtrain2,Xtest2,Ytrain2,Ytest2 = train_test_split(train,integrated[target_feature2],test_size=0.3)
    # model for available bikes : rfc_1
    rfc_1 = RandomForestRegressor(n_estimators=10
                                , random_state=90
                                , max_depth=29
                                , max_features=12
                                )
    rfc_1 = rfc_1.fit(Xtrain, Ytrain.Available_bikes)


    # model for available stands : rfc_2
    rfc_2 = RandomForestRegressor()
    rfc_2 = rfc_2.fit(Xtrain2, Ytrain2.Available_bike_stands)

    dump(rfc_1, 'avai_bike.joblib')
    dump(rfc_2, 'avai_station.joblib')

    return True

def predict_available_bike(arr):
    # arr is a list like : ["Day", "Hour", "Station_number", 'Bike_stands', 'Banking', 'Bonus', 'main', 'temp',
    #                       'feels_like', 'temp_min', 'temp_max', 'wind_speed', 'pressure', 'humidity']
    train_data = []
    train_data.append(arr)
    rfc_1 = load('avai_bike.joblib')
    rfc_2 = load('avai_station.joblib')

    available_bike = rfc_1.predict(train_data)
    available_stands = rfc_2.predict(train_data)

    result = []
    result.append(available_bike)
    result.append(available_stands)

    for i in range(len(result)):
        if result[i]-int(result[i])>0.5:
            result[i] = int(result[i])+1
        else:
            result[i]=int(result[i])



    return result

# print(save_models())
# arr = [3,1,64,40,1,0,0,5.9,1.88,5.56,6.11,4.1,1020,93]
# print("Available bike: ",predict_available_bike(arr)[0],"Available stands: ",predict_available_bike(arr)[1])



