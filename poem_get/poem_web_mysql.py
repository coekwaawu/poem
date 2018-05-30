import MySQLdb
import time
import re
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
    sql = "SELECT poem_id FROM poem;"
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


def remove_content_yi_zhu_shang_html_tag_and_return_array(str):
    pattern1 = re.compile('<br />|\n|<p.*?>|</p>|<div.*?>|</div>|<span.+?>|</span>')
    remove_htmltag_with_special_character = re.sub(pattern1, '&', str)
    pattern4 = re.compile('&\([a-z].*?\)&')
    str4 = re.sub(pattern4, '', remove_htmltag_with_special_character)
    pattern2 = re.compile('&{1,}')
    split_sentence_with_special_character = re.sub(pattern2, '&', str4)
    pattern3 = re.compile('&[0-9]{1,}、')
    str3 = re.sub(pattern3, '', split_sentence_with_special_character)
    array = re.split('&', str3)
    for item in array:
        if item == '':
            array.remove(item)
    return array


def insert_table_poem_content(poem_ids):
    db = get_mysql_db()
    cur = db.cursor()
    for poem_id in poem_ids:
        poem = get_poem_by_id_from_mysql(poem_id)
        content_array = remove_content_yi_zhu_shang_html_tag_and_return_array(poem['content'])
        order_number = 1
        for content in content_array:
            sql = "INSERT INTO poem_content (poem_id, content, order_number) VALUES (\'{}\', \'{}\', \'{}\')"\
                .format(poem_id, content, order_number)
            try:
                cur.execute(sql)
                db.commit()
                print("Success! poem_id:{}, content:{}, order_number:{}".format(poem_id, content, order_number))
            except Exception as e:
                db.rollback()
                print(e)
                print("错误! poem_id:{}, content:{}, order_number:{}".format(poem_id, content, order_number))
            order_number += 1
    cur.close()
    db.close()


def get_poem_content_id_by_poem_content(poem_content):
    db = get_mysql_db()
    cur = db.cursor()
    sql = "SELECT poem_content_id From poem_content where content = \'{}\'".format(poem_content)
    try:
        cur.execute(sql)
        poem_content_id = cur.fetchall()[0][0]
    except:
        poem_content_id = None
    cur.close()
    db.close()
    return poem_content_id


def insert_table_poem_yi(poem_ids):
    db = get_mysql_db()
    cur = db.cursor()
    for poem_id in poem_ids:
        poem = get_poem_by_id_from_mysql(poem_id)
        yi_array = remove_content_yi_zhu_shang_html_tag_and_return_array(poem['yi'])
        if len(yi_array) == 0:
            continue
        print("poem_id:{},poem_yi_count:{}".format(poem_id, len(yi_array)))
        i = 0
        reference_start = 0
        poem_content_id = 0
        for item in yi_array:
            if item != "参考资料：":
                if get_poem_content_id_by_poem_content(item) is not None:
                    poem_content_id = get_poem_content_id_by_poem_content(item)
                else:
                    yi = item
                    sql = "INSERT INTO poem_yi(poem_id, yi, poem_content_id) VALUES (\'{}\', \'{}\', \'{}\')" \
                        .format(poem_id, yi, poem_content_id)
                    try:
                        cur.execute(sql)
                        db.commit()
                        print("Insert poem_yi success!poem_id:{},poem_yi:{}".format(poem_id, item))
                    except Exception as e:
                        db.rollback()
                        print('\033[1;31m')
                        print("添加poem_yi失败!错误信息:{}".format(e))
                        print('\033[0m')
            elif item == "参考资料：":
                reference_start = i
                break
            i += 1
        if reference_start == 0:
            continue
        order_number = 1
        for j in range(reference_start+1, len(yi_array)):
            reference = yi_array[j]
            relation_table_name = "poem_yi"
            relation_poem_id = poem_id
            sql = "INSERT INTO poem_reference(reference, relation_table_name, relation_poem_id, order_number) VALUES "\
                  "(\'{}\', \'{}\', \'{}\', \'{}\')".format(reference, relation_table_name, relation_poem_id, order_number)
            try:
                cur.execute(sql)
                db.commit()
                print("Insert reference success!Reference:{}".format(reference))
            except Exception as e:
                db.rollback()
                print('\033[1;31m')
                print("添加reference错误!ErrorInfo:{}".format(e))
                print('\033[0m')
            order_number += 1
    cur.close()
    db.close()


def insert_table_poem_zhu(poem_ids):
    db = get_mysql_db()
    cur = db.cursor()
    for poem_id in poem_ids:
        poem = get_poem_by_id_from_mysql(poem_id)
        zhu_array = remove_content_yi_zhu_shang_html_tag_and_return_array(poem['zhu'])
        if len(zhu_array) == 0:
            continue
        print("poem_id:{},poem_zhu_count:{}".format(poem_id, len(zhu_array)))
        i = 0
        reference_start = 0
        poem_content_id = 0
        for item in zhu_array:
            if item != "参考资料：":
                if get_poem_content_id_by_poem_content(item) is not None:
                    poem_content_id = get_poem_content_id_by_poem_content(item)
                else:
                    zhu = item
                    sql = "INSERT INTO poem_zhu(poem_id, zhu, poem_content_id) VALUES (\'{}\', \'{}\', \'{}\')" \
                        .format(poem_id, zhu, poem_content_id)
                    try:
                        cur.execute(sql)
                        db.commit()
                        print("Insert poem_zhu success!poem_id:{},poem_zhu:{}".format(poem_id, item))
                    except Exception as e:
                        db.rollback()
                        print('\033[1;31m')
                        print("添加poem_zhu失败!错误信息:{}".format(e))
                        print('\033[0m')
            elif item == "参考资料：":
                reference_start = i
                break
            i += 1
        if reference_start == 0:
            continue
        order_number = 1
        for j in range(reference_start + 1, len(zhu_array)):
            reference = zhu_array[j]
            relation_table_name = "poem_zhu"
            relation_poem_id = poem_id
            sql = "INSERT INTO poem_reference(reference, relation_table_name, relation_poem_id, order_number) VALUES " \
                  "(\'{}\', \'{}\', \'{}\', \'{}\')".format(reference, relation_table_name, relation_poem_id,
                                                            order_number)
            try:
                cur.execute(sql)
                db.commit()
                print("Insert reference success!Reference:{}".format(reference))
            except Exception as e:
                db.rollback()
                print('\033[1;31m')
                print("添加reference错误!ErrorInfo:{}".format(e))
                print('\033[0m')
            order_number += 1
    cur.close()
    db.close()


def insert_table_poem_shang(poem_ids):
    db = get_mysql_db()
    cur = db.cursor()
    for poem_id in poem_ids:
        poem = get_poem_by_id_from_mysql(poem_id)
        shang_array = remove_content_yi_zhu_shang_html_tag_and_return_array(poem['shang'])
        if len(shang_array) == 0:
            continue
        print("poem_id:{},poem_zhu_count:{}".format(poem_id, len(shang_array)))
        i = 0
        reference_start = 0
        for item in shang_array:
            if item != "参考资料：":
                if get_poem_content_id_by_poem_content(item) is None:
                    shang = item
                    sql = "INSERT INTO poem_shang(poem_id, shang) VALUES (\'{}\', \'{}\')" \
                        .format(poem_id, shang)
                    try:
                        cur.execute(sql)
                        db.commit()
                        print("Insert poem_shang success!poem_id:{},poem_shang:{}".format(poem_id, item))
                    except Exception as e:
                        db.rollback()
                        print('\033[1;31m')
                        print("添加poem_shang失败!错误信息:{}".format(e))
                        print('\033[0m')
            elif item == "参考资料：":
                reference_start = i
                break
            i += 1
        if reference_start == 0:
            continue
        order_number = 1
        for j in range(reference_start + 1, len(shang_array)):
            reference = shang_array[j]
            relation_table_name = "poem_shang"
            relation_poem_id = poem_id
            sql = "INSERT INTO poem_reference(reference, relation_table_name, relation_poem_id, order_number) VALUES " \
                  "(\'{}\', \'{}\', \'{}\', \'{}\')".format(reference, relation_table_name, relation_poem_id,
                                                            order_number)
            try:
                cur.execute(sql)
                db.commit()
                print("Insert reference success!Reference:{}".format(reference))
            except Exception as e:
                db.rollback()
                print('\033[1;31m')
                print("添加reference错误!ErrorInfo:{}".format(e))
                print('\033[0m')
            order_number += 1
    cur.close()
    db.close()


# remove_copyright()
# update_poem_to_mysql(get_poem_ids_which_yizhushang_is_not_complete())
# print(get_remove_copyright_poem_by_id("12f82c602c43")['yizhu'])
# csv_to_mysql()

'''
content = get_poem_by_id_from_mysql("ee16df5673bc")["yi"]
array = remove_content_yi_zhu_shang_html_tag_and_return_array(content)
#print(array)
for item in array:
    print(item.strip())
'''

#insert_table_poem_yi(get_poem_ids_from_mysql())
insert_table_poem_zhu(get_poem_ids_from_mysql())
#insert_table_poem_content(get_poem_ids_from_mysql())

'''
poem_ids = get_poem_ids_which_yizhushang_is_not_complete()
for poem_id in poem_ids:
	print(poem_id)
print(len(poem_ids))
'''
