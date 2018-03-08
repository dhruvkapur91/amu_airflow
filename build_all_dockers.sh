docker build -f WebserverDockerfile -t my-airflow-presentation-webserver .
docker build -f SchedulerDockerFile -t my-airflow-presentation-scheduler .
docker build -f PostgresDockerFile  -t my-airflow-data-postgres .
docker build -f DataserverDockerFile -t my-airflow-presentation-dataserver .

