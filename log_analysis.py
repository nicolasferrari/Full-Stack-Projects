#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 11:59:43 2018

@author: Nicolas
"""

import psycopg2


def get_articles():
    
    db = psycopg2.connect('dbname=news')
    cursor = db.cursor()
    cursor.execute("select split_part(path,'/',3) as articles, count(split_part(path,'/',3)) as views from log where split_part(path,'/',3) <> '' GRUOP BY path ORDER BY views DESC limit 3")
    results = cursor.fetchall()
    print(results)
    db.close()
    
    return results

def get_bad_requests():
    
    db = psycopg2.connect('dbname=news')
    cursor = db.cursor()
    cursor.execute("select * from final_table where pct_errors > 0.01")
    results = cursor.fetchall()
    print(results)
    db.close()
    
    return results

def popular_articles():
    
    db = psycopg2.connect('dbname=news')
    cursor = db.cursor()
    cursor.execute("select sum(count) , name from article_author join article_log on split_part(title,' ',1) = split_part(articles,'-',1) GROUP BY name")
    results = cursor.fetchall()
    print(results)
    db.close()
    
    return results
    
if __name__ == "__main__":
    get_articles()
    get_bad_requests()
    popular_articles()