import pandas as pd
import xgboost as xgb

# 評価指標の計算用
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import train_test_split

# set関数で設定するように後ほど調整
model_path = './iekari/data/assess/mod_price_prediction'

try:
    from .local_settings import *
except ImportError: pass

col_filter = ['area','dist_to_nearest_station','built_year']

def _price_predict(df): #APIの中身
    # 予測モデルの読み込み
    reg = xgb.XGBRegressor()
    reg.load_model(model_path)

    return reg.predict(df)

def price_predict(query): #実際呼び出すAPI
    # query = [q1, q2, ...]

    data = []
    for q in query:
        data.append([float(q[col]) for col in col_filter])

    df = pd.DataFrame(data, columns=col_filter)
    df['year_pp']=2019-df['built_year']
    df=df.drop(['built_year'],axis=1)

    return _price_predict(df)

# def _test1():
#     pseudo_data_path = './iekari/data/assess/sample_200.csv'
#     df = pd.read_csv(pseudo_data_path) #擬似データの読み込み
#     df = df.fillna(0)
#     X = df[col_filter]

#     return _price_predict(X)

def _test2():
    q0853 = {'dist_to_nearest_station':778.63,'area':29.0,'built_year':1995} # 3238
    q1077 = {'dist_to_nearest_station':1430.52,'area':25.0,'built_year':1984} # 2852
    q2222 = {'dist_to_nearest_station':405.41,'area':29.0,'built_year':1980} # 3050
    q3844 = {'dist_to_nearest_station':596.77,'area':23.0,'built_year':1990} # 3504

    query = [q0853,q1077,q2222,q3844]
    return price_predict(query)

if __name__ == "__main__":
    # pred = _test1()
    # print(pred)
    pred = _test2()
    print(pred)
