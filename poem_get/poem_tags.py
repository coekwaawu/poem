import requests
from pyquery import PyQuery as pq
from poem_web_mysql import get_mysql_db
from poem_web_mysql import get_poem_ids_from_mysql


def get_detailpage_poem_tags_by_id(poem_id):
    target_url = "https://so.gushiwen.org/shiwenv_{}.aspx".format(poem_id)
    poempage = requests.get(target_url).text
    pq_poempage = pq(poempage)(".main3 .left .sons .tag")
    if pq_poempage.size() > 0:
        pq_tags = pq(pq_poempage[0]).text().split('，')
        poem_tags = []
        for tag in pq_tags:
            poem_tags.append(tag.strip())
        return poem_tags
    else:
        return ''


def get_detailpage_poem_tags_by_id_relation(poem_id):
    target_url = "https://so.gushiwen.org/shiwenv_{}.aspx".format(poem_id)
    poempage = requests.get(target_url).text
    pq_poempage = pq(poempage)(".main3 .left .sons .tag")
    if pq_poempage.size() > 0:
        pq_tags = pq(pq_poempage[0]).text().split('，')
        poem_tags = []
        for tag in pq_tags:
            poem_tag = {"poem_id": poem_id, "poem_tag": tag.strip()}
            poem_tags.append(poem_tag)
        return poem_tags
    else:
        return ''


def poem_tags_to_mysql():
    poem_ids = get_poem_ids_from_mysql()
    count = 0
    total_poem_ids_count = 20000
    for poem_id in poem_ids:
        if count < total_poem_ids_count:
            count += 1
            poem_tags = get_detailpage_poem_tags_by_id(poem_id)
            for poem_tag in poem_tags:
                db = get_mysql_db()
                cur = db.cursor()
                sql = "INSERT INTO poem_tag(name) VALUES(\'{}\');".format(poem_tag)
                try:
                    cur.execute(sql)
                    db.commit()
                    print("成功新增标签:{}".format(poem_tag))
                except Exception as e:
                    db.rollback()
                    print(e)
                cur.close()
                db.close()


def poem_tag_relation_to_mysql():
    db = get_mysql_db()
    cur = db.cursor()
    poem_ids = get_poem_ids_from_mysql()
    count = 0
    total_poem_ids_count = 20000
    for poem_id in poem_ids:
        if count < total_poem_ids_count:
            count += 1
            poem_tags = get_detailpage_poem_tags_by_id_relation(poem_id)
            for poem_tag in poem_tags:
                poem_id = poem_tag['poem_id']
                poem_tag_name = poem_tag['poem_tag']
                get_tag_id_sql = "SELECT poem_tag_id FROM poem_tag WHERE name = \'{}\';".format(poem_tag_name)
                get_poem_title_by_poem_id_sql = "SELECT title FROM poem WHERE poem_id = \'{}\';".format(poem_id)
                poem_title = ''
                try:
                    cur.execute(get_poem_title_by_poem_id_sql)
                    results = cur.fetchall()
                    poem_title = results[0][0]
                except Exception as e:
                    print(e)
                tag_id = ''
                try:
                    cur.execute(get_tag_id_sql)
                    results = cur.fetchall()
                    tag_id = results[0][0]
                    print(
                        "poem_id:{},poem_title:{},poem_tag_id:{},tag_name:{}".format(poem_id, poem_title, tag_id, poem_tag_name))
                except Exception as e:
                    print(e)
                sql = "INSERT INTO poem_tag(poem_id,poem_tag_id,poem_title,tag_name) VALUES(\'{}\',\'{}\',\'{}\',\'{}\');".format(
                    poem_id, tag_id, poem_title, poem_tag_name)
                try:
                    cur.execute(sql)
                    db.commit()
                    print("成功新增标签:{}".format(poem_tag))
                except Exception as e:
                    db.rollback()
                    print(e)
    cur.close()
    db.close()

# poem_tag_relation_to_mysql()
