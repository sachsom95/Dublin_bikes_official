from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from joblib import dump, load


# def predict_available_bike(Day, Hour, Station_number, Bike_stands, Banking, Bonus, main, temp, feels_like,temp_min, temp_max, wind_speed, pressure, humidity):
def save_models():
    # read dataset from csv file
    integrated = pd.read_csv("ML/Train_dataset_mar14_mar20_without_bonus.csv")
    # all the features that are used in prediction
    train_feature = ["Day", "Hour", "Station_number", 'Bike_stands', 'Banking', 'main', 'temp', 'feels_like'
        , 'temp_min', 'temp_max', 'wind_speed', 'pressure', 'humidity']
    # target 1 : available bike of source
    target_feature1 = ['Available_bikes']
    # target 2: available stands of destination
    target_feature2 = ['Available_bike_stands']

    train = integrated[train_feature]
    target = integrated[target_feature1]
    # split training and testing dataset for target 1
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(train, target, test_size=0.3)

    # split training and testing dataset for target 2
    Xtrain2,Xtest2,Ytrain2,Ytest2 = train_test_split(train,integrated[target_feature2],test_size=0.3)
    # model for available bikes : rfc_1
    rfc_1 = RandomForestRegressor(n_estimators=10
                                , random_state=0
                                , max_depth=28
                                , max_features=11
                                )
    rfc_1 = rfc_1.fit(Xtrain, Ytrain.Available_bikes)


    # model for available stands : rfc_2
    rfc_2 = RandomForestRegressor(
        n_estimators=10
        , random_state=0
        , max_depth=27
        , max_features=11
    )
    rfc_2 = rfc_2.fit(Xtrain2, Ytrain2.Available_bike_stands)
    # save models
    dump(rfc_1, 'ML/avai_bike.joblib')
    dump(rfc_2, 'ML/avai_station.joblib')

    return True

def predict_available_bike(arr):
    # arr is a list like : ["Day", "Hour", "Station_number", 'Bike_stands', 'Banking', 'Bonus', 'main', 'temp',
    #                       'feels_like', 'temp_min', 'temp_max', 'wind_speed', 'pressure', 'humidity']
    train_data = []
    train_data.append(arr)
    # load model 1
    rfc_1 = load('ML/avai_bike.joblib')

    available_bike = rfc_1.predict(train_data)

    # threshold float to integers
    if available_bike-int(available_bike)>0.5:
        available_bike = int(available_bike)+1
    else:
        available_bike=int(available_bike)
    return available_bike

def predict_available_stands(arr):
    train_data = []
    train_data.append(arr)
    # load model 2
    rfc_2 = load('ML/avai_station.joblib')
    available_stands = rfc_2.predict(train_data)
    # threshold float to integers
    if available_stands-int(available_stands)>0.5:
        available_stands = int(available_stands)+1
    else:
        available_stands=int(available_stands)
    return available_stands

# print(save_models())
# arr = [3,1,64,40,1,0,0,5.9,1.88,5.56,6.11,4.1,1020,93]
# print("Available bike: ",predict_available_bike(arr)[0],"Available stands: ",predict_available_bike(arr)[1])



