### 2 ways to build this:

## Run on your own machine:
Clone this and run the following command, you'll need `docker` and `docker-compose`
Follow [docker compose](https://docs.docker.com/compose/install/) and [docker ce (community edition)](https://docs.docker.com/install/#supported-platforms) install instructions to get these.

Then run `sh build_all_dockers.sh` to build all the relevant docker files.

+ WebserverDockerfile - is airflow webserver
+ SchedulerDockerFile - is airflow scheduler
+ PostgresDockerFile - is postgres database used for data (not airflow) webserver
+ DataserverDockerFile - is webserver used for data (not airflow)

then do `docker-compose -f docker-compose-LocalExecutor.yml up`

## Run it on aws
You'll need to register on aws, create an EC2 machine in Ohio region with the following ami id. From security groups, open port 22 for ssh and 8080 for web ui

You can also find this in an amazon AMI name: amu_docker_and_airflow
ami id: ami-4955632c
