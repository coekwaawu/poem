import MySQLdb
import time
from poem_web import get_remove_copyright_poem_by_id
from poem_web import remove_copyright_string
from poem_web_csv import get_poem_from_csv


def get_mysql_db():
    db = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='poem',
        charset='utf8'
    )
    return db


def csv_to_mysql():
    db = get_mysql_db()
    cur = db.cursor()
    poems = get_poem_from_csv()
    i = 0
    for poem in poems:
        i += 1
        if i == 100000:
            break
        else:
            sql = "INSERT INTO poem(poem_id,title,dynasty,author,content," \
                  "yi,zhu,shang,yizhu,yishang,zhushang,yizhushang)" \
                  " VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')"\
                .format(poem["poem_id"], poem["title"], poem["time"], poem["author"], poem["content"], poem['yi']
                        , poem['zhu'], poem['shang'], poem['yizhu'], poem['yishang'], poem['zhushang']
                        , poem['yizhushang'])
            try:
                cur.execute(sql)
                db.commit()
                print("成功添加 {} 到数据库".format(poem["title"]))
            except Exception as e:
                print(e)
                db.rollback()
    db.close()


def get_poem_ids_from_mysql():
    db = get_mysql_db()
    cur = db.cursor()
    sql = "SELECT poem_id FROM poem WHERE yizhushang=\'\';"
    poem_ids = []
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            poem_ids.append(row[0])
    except Exception as e:
        print(e)
    cur.close()
    db.close()
    return poem_ids


def get_poem_by_id_from_mysql(poem_id):
    db = get_mysql_db()
    cur = db.cursor()
    sql = "SELECT * FROM poem WHERE poem_id=\'{}\';".format(poem_id)
    poems = []
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            poem = {
                "poem_id": row[0],
                "title": row[1],
                "dynasty": row[2],
                "author": row[3],
                "content": row[4],
                "yi": row[5],
                "zhu": row[6],
                "shang": row[7],
                "yizhu": row[8],
                "yishang": row[9],
                "zhushang": row[10],
                "yizhushang": row[11]
            }
            poems.append(poem)
    except Exception as e:
        print(e)
    cur.close()
    db.close()
    return poems[0]


def update_poem_to_mysql(poem_ids):
    start_time = time.clock()
    poem_count = 0
    count_for_sleep = 0
    sleep_time = 0
    db = get_mysql_db()
    cur = db.cursor()
    for poem_id in poem_ids:
        poem_count += 1
        poem = get_remove_copyright_poem_by_id(poem_id)
        if poem is not None:
            sql = "UPDATE poem SET title=\'{}\',dynasty=\'{}\',author=\'{}\'," \
                  "content=\'{}\',yi=\'{}\',zhu=\'{}\',shang=\'{}\',yizhu=\'{}\'," \
                  "yishang=\'{}\',zhushang=\'{}\',yizhushang=\'{}\' WHERE poem_id=\'{}\';"\
                .format(poem['title'], poem['dynasty'], poem['author'], poem['content'], poem['yi'], poem['zhu']
                        , poem['shang'], poem['yizhu'], poem['yishang'], poem['zhushang'], poem['yizhushang']
                        , poem['poem_id'])
            try:
                cur.execute(sql)
                db.commit()
                print("更新第 {} 首诗词: {} 成功。".format(poem_count, poem["title"]))
            except Exception as e:
                db.rollback()
                print(e)
                print("update_poem_to_mysql error,poem_id:{}".format(poem_id))
            count_for_sleep += 1
            if count_for_sleep == 10:
                run_time = time.clock() - start_time
                print("已更新诗词 10 首,程序已运行 {} 秒,请等待 {} 秒.".format(run_time, sleep_time))
                time.sleep(sleep_time)
                count_for_sleep = 0
    cur.close()
    db.close()


def remove_copyright():
    db = get_mysql_db()
    cur = db.cursor()
    get_poem_sql = "SELECT * FROM poem;"
    try:
        cur.execute(get_poem_sql)
        results = cur.fetchall()
        poem_count = 1
        for row in results:
            poem_id = row[0]
            title = row[1]
            dynasty = row[2]
            author = row[3]
            content = row[4]
            yi = row[5].strip()
            zhu = row[6].strip()
            shang = row[7].strip()
            yizhu = row[8].strip()
            yishang = row[9].strip()
            zhushang = row[10].strip()
            yizhushang = row[11].strip()

            update_poem_sql = "UPDATE poem SET title=\'{}\',dynasty=\'{}\',author=\'{}\',\
			content=\'{}\',yi=\'{}\',zhu=\'{}\',shang=\'{}\',yizhu=\'{}\',\
			yishang=\'{}\',zhushang=\'{}\',yizhushang=\'{}\' WHERE poem_id=\'{}\';" \
                .format(remove_copyright_string(title), remove_copyright_string(dynasty),
                        remove_copyright_string(author), remove_copyright_string(content), remove_copyright_string(yi),
                        remove_copyright_string(zhu), remove_copyright_string(shang), remove_copyright_string(yizhu),
                        remove_copyright_string(yishang),
                        remove_copyright_string(zhushang), remove_copyright_string(yizhushang),
                        remove_copyright_string(poem_id))
            try:
                cur.execute(update_poem_sql)
                db.commit()
                print("更新第 {} 首诗词: {} 成功。".format(poem_count, title))
            except Exception as e:
                db.rollback()
                print(e)
                print("update_poem_to_mysql error,poem_id:{}".format(poem_id))
            poem_count += 1
    except Exception as e:
        print(e)
    cur.close()
    db.close()


def get_poem_ids_which_yizhushang_is_not_complete():
    sql = "SELECT poem_id FROM poem.poem " \
          "WHERE(zhu <> \"\" OR yi <> \"\" OR shang <> \"\" OR yizhu <> \"\" " \
          "OR yishang <> \"\" OR zhushang <> \"\" OR yizhushang <> \"\") " \
          "AND poem_id NOT IN (SELECT poem_id FROM poem.poem WHERE zhu <> \"\" AND yi <> \"\" AND shang <> \"\" " \
          "AND yizhu <> \"\" AND yishang <> \"\" AND zhushang <> \"\" AND yizhushang <> \"\")"
    db = get_mysql_db()
    cur = db.cursor()
    poem_ids = []
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for row in results:
            poem_ids.append(row[0])
    except Exception as e:
        print(e)
    cur.close()
    db.close()
    return poem_ids


# remove_copyright()
# update_poem_to_mysql(get_poem_ids_which_yizhushang_is_not_complete())
# print(get_remove_copyright_poem_by_id("12f82c602c43")['yizhu'])
# csv_to_mysql()
# print(len(get_poem_by_id_from_mysql("000f7224659f")["zhu"]))

'''
poem_ids = get_poem_ids_which_yizhushang_is_not_complete()
for poem_id in poem_ids:
	print(poem_id)
print(len(poem_ids))
'''
