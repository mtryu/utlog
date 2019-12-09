import pandas as pd
import numpy as np

class Cross_Tabulated_Data():

    def __init__(self):
        self.log_inpath = "ScoreLog.csv"
        self.user_inpath = "Profile.csv"
        self.estate_inpath = "Rest.csv"
        self.cross_outpath = "Cross.csv"
    
    def main(self, console = False):
        """
        データ
        scorelog：ScoreLog.csv
        profile：Profile.csv
        rentroom：RentRoom.csv
        流れ
        １　データ読み込み：self.read_data()
        ２　集計を格納する枠組み付与(ユーザ×物件)(ユーザのデモグラ情報はここで結合)：self.make_cross_flame()
        ３　scorelogより(ユーザ,物件,評価点)の組み合わせを取得し、２に格納：self.make_cross_result()
        """
        scorelog, profile, rentroom, usernum, estatenum = self.read_data()
        crossflame = self.make_cross_flame(profile, rentroom, usernum, estatenum)
        crossflame = self.make_cross_result(scorelog, crossflame)
        crossflame.to_csv(self.cross_outpath, index = False, encoding = "utf-8")

        if console == True :
            print(estatenum, usernum)
            print(profile.head(2))
            print(scorelog.tail(10))
            print(rentroom.head(2))
            print(crossflame.head(3))

    def read_data(self):
        scorelog = pd.read_csv(self.log_inpath, encoding = "utf-8")
        profile = pd.read_csv(self.user_inpath, encoding = "utf-8")
        rest = pd.read_csv(self.estate_inpath, encoding = "utf-8")
        estatenum = len(rest)
        usernum = len(profile)

        return scorelog, profile, rest, usernum, estatenum
        
    def make_cross_flame(self, profile, rest, usernum, estatenum):
        """
        rentroomとprofileの長さから格納用フレームを作成
        userのデモグラ情報はprofileと結合することで付与する
        """
        col_estate = rest["id"].values.tolist()
        index_use = np.arange(usernum)
        crossflame = pd.DataFrame(index=index_use, columns=col_estate)
        crossflame = pd.concat([profile, crossflame], axis = 1)

        return crossflame

    def make_cross_result(self, scorelog, crossflame):
        """
        クロス集計の実施
        scorelogから一行ずつ読み込んで、(ユーザ,物件,評価点)の組み合わせを取得
        (ユーザ,物件)からクロス集計用フレームの位置を指定し、評価点を格納
        """
        print("making cross data ...")
        for i in range(len(scorelog)):
            user_id = scorelog.iat[i, 0]
            es_id = scorelog.iat[i, 3]
            user_id = int(user_id[1:])
            es_id = int(es_id[1:])
            score = scorelog.iat[i, 0]
            crossflame.iat[user_id - 1, es_id - 1 + 4] = score

        crossflame = crossflame.fillna(0)

        return crossflame

if __name__ == '__main__':
    ctd = Cross_Tabulated_Data()
    ctd.main(console=True)
