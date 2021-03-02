#! /usr/bin/python3

import requests, csv

headers = {
    "Host": "pinklotto.co.zw",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "63",
    "Origin": "https://pinklotto.co.zw",
    "Connection": "close",
    "Referer": "https://pinklotto.co.zw/lotto_results",
    "Sec-GPC": "1",
    "DNT": "1",
}

data = "from_date=01%2F01%2F2011&to_date=01%2F03%2F2021&game_group_id=4"

try:
    response = requests.post(
        "https://pinklotto.co.zw/api/pinklotto/viewResult",
        headers=headers,
        data=data,
        verify=False,
    )
    results_data = response.json()["ResultData"]

    counter = 0
    rows = []

    with open("winning_balls_draws.csv", "w") as _file:
        # create the csv writer object
        csv_writer = csv.writer(_file)
        if counter == 0:
            # Writing headers of CSV file
            header = ["DrawDate", "GameName", "DrawNumber", "WinningNumber"]
            csv_writer.writerow(header)
            counter += 1
        # Writing data of CSV file
        for row in results_data:
            rows = [
                row["DrawDate"],
                row["GameName"],
                row["DrawNumber"],
                row["WinningNumber"],
            ]
            csv_writer.writerow(rows)
    with open("winning_balls.csv", "w") as _file2:
        # TODO: add last drawn column
        # Deriving the idea from https://africalotto.co.zw
        headers2 = ["Ball", "Frequency"]
        csv_writer2 = csv.writer(_file2)
        counter2 = 0
        if counter2 == 0:
            csv_writer2.writerows(headers2)
            counter += 1
        balls = set()
        ball_counter = 0
        for row in results_data:
            line = list(map(int, row["WinningNumber"].split(",")))

            balls.update(line)
            balls_data = dict()
            for l in line:
                if l in balls:
                    balls_data.update({l: ball_counter})
                    ball_counter += 1
                    continue
        print(balls_data)


except Exception as e:
    print(e)
