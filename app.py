from flask import Flask, request, json
from celery import Celery
import requests


app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

# function that will go inside celery as task
def add_2numbers(x,y):
    return x+y


# task initialise in celery
@celery.task()
def add(x, y):
    res = add_2numbers(x,y)
    return res




@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        x = 5
        y = 10
        if x and y:
            # use celery task funtion in route along with delay method.
            res = add.delay(x,y)
            print(res)
            return json.dumps({
                    'ID' : res.id,
                    'Status' : 'Queued'

                }) 

# Get the status using this route
@app.route('/result/<task_id>')
def taskid(task_id):
    output = celery.AsyncResult(task_id)  
    print(output)        
    if output.state == 'SUCCESS':
        main_output = output.get()
        print(main_output)

        return json.dumps({
            'Task Id' : task_id,
            'Queue Status' : 'Completed',
            'Output' : output.get()
        })

    elif output.state == 'PENDING':
        print(output.status)
        return json.dumps({
            'TaskId' : task_id,
            'Queue Status' : 'Queued'
        })
    else:
        return json.dumps({
            'TaskId' : task_id,
            'Queue State' : output.state,
            'Details' : str(output.info)
        })
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)

# python3 celery -A app.celery worker --loglevel=DEBUG