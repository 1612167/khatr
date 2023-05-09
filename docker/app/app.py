import time
import pandas as pd
import redis
from flask import Flask, render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)
@app.route('/titanic')
def titanic():
    # load the CSV file using pandas
    df = pd.read_csv('titanic.csv')

    # create HTML table using the first 5 rows of the CSV data
    table = df.head().to_html(index=False)

    # render the titanic.html template with the table variable
    return render_template('titanic.html', table=table)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)