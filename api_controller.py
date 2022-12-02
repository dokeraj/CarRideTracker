import json

from flask import Flask, abort, Response, request

import sqliteDatabase

app = Flask("FlaskApp")


@app.route("/api/getUsersAndCounts", methods=['GET'])
def getUsersAndCounts():
    usersAndCounts = sqliteDatabase.get_users_and_counts()
    jsonResponse = json.dumps(usersAndCounts)

    return Response(jsonResponse, mimetype='application/json')


@app.route("/api/deleteRecord/<record_id>", methods=['DELETE'])
def deleteRecord(record_id):
    delete_successful = sqliteDatabase.delete_record(record_id)

    if delete_successful:
        return Response(json.dumps({"Success": "Record deleted"}), status=202, mimetype='application/json')
    else:
        return abort(
            Response(json.dumps({"Error": "Record cannot be deleted!"}), status=400, content_type='application/json'))


# This API has a query string parameter `timestamp`
@app.route("/api/updateRecord/<record_id>", methods=['PATCH'])
def updateRecord(record_id):
    input_json = request.json

    if "user" not in input_json or "timestamp" not in input_json:
        errResp = json.dumps({"Error": "Cannot update! User or Timestamp field in body is not present!"})
        return abort(Response(errResp, status=400, content_type='application/json'))

    update_successful = sqliteDatabase.update_record(record_id, input_json.get("user"), input_json.get("timestamp"))

    if update_successful:
        return Response(json.dumps({"Success": "Record updated"}), status=202, mimetype='application/json')
    else:
        return abort(
            Response(json.dumps({"Error": "Record cannot be updated!"}), status=400, content_type='application/json'))


@app.route("/api/insertRecord", methods=['POST'])
def insertRecord():
    input_json = request.json

    if "user" not in input_json or "timestamp" not in input_json:
        errResp = json.dumps({"Error": "User or Timestamp field in body is not present!"})
        return abort(Response(errResp, status=400, content_type='application/json'))

    insert_successful = sqliteDatabase.insert_record(input_json.get("user"), input_json.get("timestamp"))

    if insert_successful:
        return Response(json.dumps({"Success": "Record created"}), status=201, mimetype='application/json')
    else:
        return abort(
            Response(json.dumps({"Error": "Record not created!"}), status=400, content_type='application/json'))


# This API has a query string parameters `from` and `size`
@app.route("/api/listRecords", methods=['GET'])
def listRecords():
    start_from = request.args.get("from", default=0)
    size = request.args.get("size", default=10)
    sorting = request.args.get("sortingDesc", default='true')

    if sorting == 'false':
        sorting = "ASC"
    else:
        sorting = "DESC"

    records, total = sqliteDatabase.get_logs(start_from, size, sorting)

    return Response(json.dumps({"records": records, "total": total}), status=200, mimetype='application/json')


def runApi():
    from waitress import serve
    serve(app, host='0.0.0.0', port=3050)
