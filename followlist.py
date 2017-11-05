# -*- coding: utf-8 -*-

import csv, json, config
from datetime import datetime
from requests_oauthlib import OAuth1Session
USER = "thinceller"

### Constants
oath_key_dict = {
    "consumer_key": config.CONSUMER_KEY,
    "consumer_secret": config.CONSUMER_SECRET,
    "access_token": config.ACCESS_TOKEN,
    "access_token_secret": config.ACCESS_TOKEN_SECRET
}

### Function
def main():
    list = followlist(USER, oath_key_dict)

    # ファイル名作成
    date = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = USER + "_" + date + ".csv"

    # 書き込みモードでファイル展開
    with open("out/" + file_name, "w") as csvfile:
        writer = csv.writer(csvfile, lineterminator="\n")
        writer.writerow(["名前", "ユーザID", "固有ID"])

        for account in list:
            # 一度encode()でオプション付きでbyte型に変換してからstrに戻す
            name = account["name"].encode("cp932", "ignore")
            screen_name = account["screen_name"].encode("cp932", "ignore")
            id_str = account["id_str"].encode("cp932", "ignore")

            name = name.decode("cp932")
            screen_name = screen_name.decode("cp932")
            id_str = id_str.decode("cp932")

            list = [name, screen_name, id_str]
            writer.writerow(list)
    print("Success!")
    return

def create_oath_session(oath_key_dict):
    """Create OAuth1 Session from oath_key_dict."""
    oath = OAuth1Session(
        oath_key_dict["consumer_key"],
        oath_key_dict["consumer_secret"],
        oath_key_dict["access_token"],
        oath_key_dict["access_token_secret"]
    )
    return oath

def followlist(screen_name, oath_key_dict):
    """Get all followlist by screen_name."""
    followlist = []
    next_cursor = -1
    url = "https://api.twitter.com/1.1/friends/list.json"

    while True:
        params = {
            "screen_name": screen_name,
            "count": "200",
            "cursor": next_cursor
        }
        oath = create_oath_session(oath_key_dict)
        res = oath.get(url, params = params)

        # エラー処理
        if res.status_code != 200:
            print("ERROR: %d" % res.status_code)
            return None

        list = json.loads(res.text)
        next_cursor = list["next_cursor"]
        followlist += list["users"]

        # カーソルが0、つまり最後のページになればループを抜ける
        if next_cursor == 0:
            break

    return followlist

### Excute
if __name__ == "__main__":
    main()
