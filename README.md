# Full-Stack-Projects

1st QUESTION: 

The first question of the project is answered with a a select statement that look in the log table for the articles that are the most visited by the users of the site. The query is as follow: 

  select split_part(path,'/',3) as articles, count(split_part(path,'/',3)) as views from log where split_part(path,'/',3) <> '' GROUP BY    path ORDER BY views DESC limit 3;

  The split_part() command is used first in order to split the path field in the log tables by the '/' character and take the third word  that have the article description. So I tranform the path to the articles field using split_part. Secondly in order to sum articles , I used another time split_part but in this time with the count command, to count the unique number of path. I named this field to views. 

  The condition that this statement has is that split_part(path, '/', 3) must be <> '' as there are many empty string in the path field. Lastly I group by the statement on the path field and show the results in descending order meaning that the most viewed articles are first. 

2nd QUESTION: 

For the second question I created two views. The first was denominated article_log and consist in : 

CREATE VIEW art_log as select count(split_part(path, '/',3)), split_part(path,'/',3) as articles from log GROUP BY articles HAVING COUNT(split_part(path, '/',3)) > 1000;
 
This view show 2 fields. The first field count the numbers of each path in the log table, and the second field show the name of the article(using split_part I remove the /articles/ part of the path field). Then the statement group by the articles temporary field and lastly use the HAVING command to filter the path that repeat more than 1000 times. The aim of the HAVING command is to remove bad or misspelled path fields in the log table.

The second view that I created to answer this question is the following:

CREATE VIEW art_author as select title, name, slug from articles join authors on articles.author = authors.id 
This view is a join between the authors table and the articles table. The aim of this view is to join information between the two tables and to bring the slug field that has the same string pattern than the path field of the log table.


The statement that are in the code file is the following: 

select sum(count) , name from art_author join art_log on art_author.slug = art_log.articles GROUP BY name;

This statement sum the count field for each author from the art_log view and show the name of the article from the art_author view. For this it was necessary to join the two views using the slug field from the art_author view and the articles(temporary field) from the art_log vies.




3rd QUESTION: 

For the third question of the project I created three views. The first view is called wrong_requests that is as follow: 

  CREATE VIEW wrong_requests as select time::date as date , COUNT(status) as error_requests from log where status != '200 OK' GROUP BY date, status;

  This view sum up the bad requests that happened in each day. The view has two fields that are date and error_requests that means the number of errors requests on each day. In this view I filter the statement for all the rows that have status distinct from '200 OK'.

The second view that I created in the third question is called rigth_requests that consist in:

  CREATE VIEW rigth_requests as select time::date as date, COUNT(status) as good_requests from log where status= '200 OK' GROUP BY date, status;

This view has the same goal of the first view, but in this case, the final output are the total of correct requests from each day. I filter with the status equal to 200 OK to only work with the good requests in the log table. 

The third view that I created is a combination of the first and second views: 

CREATE VIEW errors_good_requests as select rigth_requests.date, ROUND(cast(error_requests as decimal(7,2)) / cast(good_requests as      decimal(7,2)) ,4) as pct_errors from rigth_requests join wrong_requests on rigth_requests.date = wrong_requests.date;

This view make the division between bad requests(error_requests field) and good requests(good_requests field) and call this field as pct_errors. To make this view, it was necessary to join the rigth_requests view with the wrong_requests view by the date field in order to have information for the same date in both tables. 

The final statement is :  select * from errors_good_requests where pct_errors > 0.01; that filter the errors_good_requests view for the rows or days that have a ratio of bad/good requests greater than 1%.



