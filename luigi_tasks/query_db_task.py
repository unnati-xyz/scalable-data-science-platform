import luigi
import psycopg2

class QueryPostgresTask(luigi.Task):
    def output(self):
        # the output will be a .csv file
        return luigi.LocalTarget("sample_trip.csv")

    def run(self):
        # these are here for convenience, you'll use
        # environment variables for production code
        host = "localhost"
        database = "bike_share"
        user = "postgres"
        password = "postgres"

        conn = psycopg2.connect(
            dbname=database,
            user=user,
            host=host,
            password=password)
        cur = conn.cursor()
        cur.execute("""SELECT *
          FROM trips limit 1000 """)
        rows = cur.fetchall()

        with self.output().open("w") as out_file:
            # write a csv header 'by hand'
            out_file.write("trip_id, duration, start_date, start_station, start_terminal, \
            end_date, end_station, end_terminal, bike_num, subscription_type, zipcode")

            for row in rows:
                out_file.write("\n")
                # without the :%s, the date will be output in year-month-day format
                # the star before row causes each element to be placed by itself into format
                out_file.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(*row))
