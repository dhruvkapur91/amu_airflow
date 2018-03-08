Run `sh build_all_dockers.sh` to build all the relevant docker files.

+ WebserverDockerfile - is airflow webserver
+ SchedulerDockerFile - is airflow scheduler
+ PostgresDockerFile - is postgres database used for data (not airflow) webserver
+ DataserverDockerFile - is webserver used for data (not airflow)

then do `docker-compose -f docker-compose-LocalExecutor.yml up`

