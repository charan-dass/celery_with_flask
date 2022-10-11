# Basic Code of Celery Task Queue with flask.

Use this code to implement celery in your application.

#
# !Note Redis or RabitMQ must install on your machine as celery requires a broker to run.
in this application, we will be using Redis.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install flask
pip install celery
pip install redis
```
Or install 

```bash
pip install -r requirements.txt
```

## Usage
For demonstration, we will use add_2numbers() function. you can use your own function.
 In app.py there is a function called add_2numbers() which will be used in celery as a task.

```bash
# function that will go inside celery as a task
def add_2numbers(x,y):
    return x+y
```

Assign the above function to celery.
#
# Task initialize in celery
you can create your own function below `@celery.task()` decorator and initialize your own task.

```bash
# task initialize in celery
@celery.task()
def add(x, y):
    res = add_2numbers(x,y) # function assign to variable as task
    return res
```

#
# Now we will use this `add()` task in our home route
```bash
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        x = 5
        y = 10
        if x and y:
            # use celery task function in route along with delay method.
            res = add.delay(x,y)
            print(res)
            return json.dumps({
                    'ID' : res.id,
                    'Status' : 'Queued'

                }) 
```
#
# To get the result we have created a different route.
```bash
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

```
# 
# command to run flask application in terminal 
```bash
python3 app.py
```
# Use another terminal and run celery using the command.
```bash
python3 celery -A app.celery worker --loglevel=DEBUG
```