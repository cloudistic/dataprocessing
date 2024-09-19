## Apache Spark - Demo
    * Go to Spark docker directory
        $cd ~/docker/apache-spark
    * Make sure docker service is running
        $sudo systemctl status docker.service
    * Find the list of containers running
        $sudo docker ps
    * Start the spark containers
        $sudo docker-compose up -d
            Creating network "apache-spark_default" with the default driver
            Creating apache-spark_spark-master_1 ... done
            Creating apache-spark_spark-worker-2_1 ... done
            Creating apache-spark_spark-worker-1_1 ... done
    * Copy the sparktest.py to master node
        $ sudo docker cp -L sparktest.py apache-spark_spark-master_1:/opt/bitnami/spark/sparktest.py
            Among all the log messages there should be an output similar to the following
                THE SUM IS HERE:  499500
    * Exercise: Create a word count program using pySpark and execute it in the cluster.
    * Stop the containers
         $sudo docker-compose down
## Apache Kafka - Demo ( Producer / Consumer )
    * Go to Kafka container directory
        $cd ~/docker/apache-kafka
    * Make sure docker service is running
        $sudo systemctl status docker.service
    * Find the list of containers running
        $sudo docker ps
    * Start the Kafka container
        $sudo docker-compose up -d

    * Create a topic called "purchases"
        $sudo docker exec --workdir /opt/kafka/bin/ -it broker sh
        
        Inside the docker container list the available topics
            ./kafka-topics.sh --list --bootstrap-server localhost:9092
        
        Inside the docker container create a topic

            ./kafka-topics.sh --create --topic purchases --bootstrap-server localhost:9092

    * Install Kakfa python library
        $pip install confluent-kafka
    * Open a terminal and run the consumer.py
    * Open another terminal and run producer.py

    * Exercise: Change the type of message, create a new topic, increase the number of messages
    * Stop the container
        $sudo docker-compose down

## Ray and Dask - Demo
    * Go to Ray and Dask program directory
        $cd ~/distributed
    * Create a python environment and install Ray module
        $pip install -U "ray[default]"
    * Download the data files to the directory where the ray-program.py is present
        https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/1980.tar.gz
        https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/2020.tar.gz
    * Run the Ray example program
        $python ray-program.py
        This should start a Ray instance, load the zip file with 2 workers
        Try to browse http://127.0.0.1:8265 while the program is running. This will show the progress and the number of jobs.
    * Run the dask-program.py
        $python dask-program.py
        This will load the file "Sunsports.csv" and print the time taken.
    * Exercise
        1. Download a new data file from https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/2021.tar.gz
        2. Increase the number of Ray workers from 2-3 and show the results.
        3. Duplicate the entries in "Sunspots.csv"
        4. Run the dask-program.py to see how the Dask Data frames is performing when the data increases.
## Postgres and Grafana
    * Go to PostgreSQL docker directory
        $cd ~/docker/postgresql
    * Make sure docker service is running
        $sudo systemctl status docker.service
    * Find the list of containers running
        $sudo docker ps
    * Start the PostgreSQL docker container
        $sudo docker-compose up -d
    * Copy the data file inside docker container
        $sudo docker cp -L testdata.csv postgresql_postgresql_1:/tmp/testdata.csv
    * Go inside the container and create a table
        $ psql -U postgres
        postgres=# \c postgres
        postgres=# ALTER USER postgres WITH PASSWORD 'yourpass';
        postgres=# CREATE TABLE t_oil (region      text,country     text,year        int,production  int,consumption int);
        postgres=# COPY t_oil FROM '/tmp/testdata.csv' WITH (FORMAT csv);
        postgres=# SELECT * from t_oil;
    
    * Pull the Grafana container
        $sudo docker pull grafana/grafana
    * Start the Grafana container
        $sudo docker run -d -p 3000:3000 --name=grafana grafana/grafana
    * Reset the Grafana Password
    * Once you are inside the Grafana, Go to Data Source and select PostgreSQL.
    * Update the postgreSQL server, port, username and password.
    * Ensure that the connection is working as expected.
    * Create a line graph with the following query
        SELECT 
            year as "time",
            production
        FROM t_oil
        WHERE
            country = 'USA'
    * See the line graph created
    * Exercise: Try adding more graphs as you see fit.
