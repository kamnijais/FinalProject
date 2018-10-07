maxMonthsCon = cursor.execute('select max(months.consumption) from months WHERE months.user_id=?', (current_user[0],))
jsonMaxMonthData = json.dumps(maxMonthsCon)

###select min(months.timestamp) from months WHERE months.user_id
minMonthsTimest = cursor.execute('select min(months.timestamp) from months WHERE months.user_id=?', (current_user[0],))
jsonMinMoTimest = json.dumps(minMonthsTimest)

maxMonthsTimest = cursor.execute('select max(months.timestamp) from months WHERE months.user_id=?', (current_user[0],))
jsonMaxMoTimest = json.dumps(maxMonthsTimest)

##select min(months.temperature) from months WHERE months.user_id
minMonthsTemp = cursor.execute('select min(months.temperature) from months WHERE months.user_id=?', (current_user[0],))
jsonMinMoTemp = json.dumps(minMonthsTemp)

maxMonthsTemp = cursor.execute('select max(months.temperature) from months WHERE months.user_id=?', (current_user[0],))
jsonMaxMoTemp = json.dumps(maxMonthsTemp)

minDaysCons = cursor.execute('select min(days.consumption) from days WHERE days.user_id=?', (current_user[0],))
jsonMinDaysData = json.dumps(minDaysCons)

maxDaysCons = cursor.execute('select max(days.consumption)  from days WHERE days.user_id =?', (current_user[0],))
jsonMaxDayData = json.dumps(maxDaysCons)

maxDaysTimest = cursor.execute('select  max(days.timestamp)  from days WHERE days.user_id =?', (current_user[0],))
jsonMaxDayTimest = json.dumps(maxDaysTimest)

minDaysTimest = cursor.execute('select  min(days.timestamp)  from days WHERE days.user_id =?', (current_user[0],))
jsonMinDayTimest = json.dumps(minDaysTimest)

minDaysTemp = cursor.execute('select  min(days.temperature)  from days WHERE days.user_id =?', (current_user[0],))
jsonMinDayTemp = json.dumps(minDaysTemp)

maxDaysTemp = cursor.execute('select  max(days.temperature)  from days WHERE days.user_id =?', (current_user[0],))
jsonMaxDayTemp = json.dumps(maxDaysTemp)

#######finalJson=jsonify({'jsonMaxDayData,jsonMaxMonthData,jsonMinDaysData,jsonMinMonthData' })
#######return jsonify({'limits' : finalJson})
return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>
                  <h1>The website value is: {}'''.format(jsonMinMonthData, jsonMaxMonthData, jsonMaxDayTemp)


##########
@app.route('/data')
@token_required
def getReqData(current_user):
    start = request.args.get('start')
    count = request.args.get('count')
    resolution = request.args.get('resolution')           # request = start=2014-03-01&count=8&resolution=M


    #SELECT  trim(timestamp, "00:00:00"), days.consumption,days.temperature FROM days WHERE days.user_id='1' LIMIT 3;
    connection = db.engine.raw_connection()
    cursor = connection.cursor()
    if resolution=="M":
        cursor.execute('select trim(months.timestamp, "00:00:00") , months.consumption, months.temperature from months where months.timestamp>? and months.user_id=? limit ?,?' , (start,count,))


    cursor.execute('SELECT  trim(timestamp, "00:00:00"), months.consumption,months.temperature FROM months WHERE months.user_id=? LIMIT ?;', (start, count,))


## sub string function =x[:-2] from back 2 indexes

    return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>
                  <h1>The website value is: {}'''.format(start, count, resolution)
