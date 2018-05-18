import csv
import time
import os
from poem_web import get_listpage_poem_ids
from poem_web import get_poem_by_id


def get_poem_ids_from_csv():
    poem_ids = []
    with open('poem.csv', 'a+', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            poem_ids.append(row["poem_id"])
    f.close()
    return poem_ids


def get_poem_to_csv():
    start_time = time.clock()
    count_for_sleep = 0
    sleep_time = 0
    exist_poem_ids = get_poem_ids_from_csv()
    headers = ["poem_id", "title", "time", "author", "content", "yi", "zhu", "shang", "yizhu", "yishang", "zhushang",
               "yizhushang"]
    with open('poem.csv', 'a+', encoding='utf-8') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for i in range(1, 1010):
            poem_count = (i - 1) * 10
            poem_ids = get_listpage_poem_ids(i, i)
            for poem_id in poem_ids:
                poem_count += 1
                if poem_id not in exist_poem_ids:
                    poem = get_poem_by_id(poem_id)
                    writer.writerow(poem)
                    print("正在获取第 {} 首诗词:{}".format(poem_count, poem["title"]))
                    count_for_sleep += 1
                    if count_for_sleep == 10:
                        run_time = time.clock() - start_time
                        print("已获取新诗词 10 首,现在检索的是第 {} 页,程序已运行 {} 秒,请等待 5 秒.".format(i, run_time))
                        time.sleep(sleep_time)
                        count_for_sleep = 0
                else:
                    print("{},poem_id:{} is already exist.".format(poem_count, poem_id))
    f.close()


def get_poem_from_csv():
    poems = []
    path = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)) + "\\poem_backup\\"
    with open(path + 'poem20180415.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            poem = {"poem_id": row["poem_id"], "title": row["title"], "time": row["time"], "author": row["author"],
                    "content": row["content"], "yi": row["yi"], "zhu": row["zhu"], "shang": row["shang"], "yizhu": "",
                    "yishang": "", "zhushang": "", "yizhushang": ""}
            try:
                poem["yizhu"] = row["yizhu"]
                poem["yishang"] = row["yishang"]
                poem["zhushang"] = row["zhushang"]
                poem["yizhushang"] = row["yizhushang"]
            except Exception as e:
                print(e)
            poems.append(poem)
        return poems

# get_poem_to_csv()
