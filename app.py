from asyncio.windows_events import NULL
from flask import json, Flask, request
app=Flask(__name__) 

jsonStr= """
{
    "result": [
        {"id": 1, "name": "name", "status": 0}
    ]
}
"""
myJson = json.loads(jsonStr)


@app.route("/") # 函式的裝飾 (Decorator)
def home():
    return "hello"

@app.route('/tasks', methods=['GET']) 
def getTasks(): 
    return myJson


@app.route('/task',  methods=['POST', 'PUT']) 
def postTask():
    reqJson = request.get_json()
    global myJson
    res = { "result" : reqJson }

    if request.method == 'POST': 

        # this block is handled by db 
        maxId = 0
        for obj in myJson['result']:
            if(maxId<obj['id']):
                maxId = obj["id"]


        reqObj ={
            "name": reqJson["name"],
            "status": 0,
            "id": maxId+1
        }
        myJson['result'].append(reqObj)

        res = { "result" : reqObj }
        return (res, 201)

        

    elif request.method == 'PUT': 

        reqName = reqJson["name"]
        reqStatus = reqJson["status"]
        reqId = reqJson["id"]

        for obj in myJson['result']:
            if(reqId == obj['id']):
                obj["status"] = reqStatus
                obj["name"] = reqName
                obj["id"] = reqId

                res = { "result" : obj }
                return res

        return (res, 404)


@app.route('/task/<int:id>', methods=['DELETE']) 
def deleteTask(id):


    for obj in myJson['result']:
        if(id == obj['id']):
            myJson['result'].remove(obj)
            return ('', 200)

    return ('', 404)


if __name__=="__main__": #如果以主程式執行
    app.run() # 立刻啟動伺服器