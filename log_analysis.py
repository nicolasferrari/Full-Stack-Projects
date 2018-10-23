#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 11:59:43 2018

@author: Nicolas
"""
import psycopg2

try:
    db = psycopg2.connect('dbname=news')
except:
    print("Unable to connect to the database")


def get_articles():

    cursor = db.cursor()
    cursor.execute("""select split_part(path,'/',3) as articles, COUNT(path)
    as views from log where split_part(path,'/',3) <> ''
    GROUP BY path ORDER BY views DESC LIMIT 3""")

    results = cursor.fetchall()
    for item in results:
        print(str(item[0]).replace('-', ' ') + ' ' +
              'with ' ' {}'.format(item[1]) + ' ' + 'views')

    return results


def get_bad_requests():

    cursor = db.cursor()
    cursor.execute("select * from final_table where pct_errors > 0.01")
    results = cursor.fetchall()
    date = results[0][0]
    str_date = '{:%B %d, %Y}'.format(date)
    errors = results[0][1]
    print(str_date + ' -- ' + '{:.2%}'.format(errors) + ' errors')

    return results


def popular_articles():

    cursor = db.cursor()
    cursor.execute("""select sum(count) , name from art_log
    join art_author on art_log.articles = art_author.slug
    GROUP BY name""")

    results = cursor.fetchall()
    authors = []
    for item in results:
        authors.append(item[1] + '  ' + '--' + '  ' +
                       '{}'.format(item[0]) + ' ' + 'views')
    authors = sorted(authors, reverse=True)
    for item in authors:
        print(item)

    db.close()

    return results

if __name__ == "__main__":
    get_articles()
    get_bad_requests()
    popular_articles()
