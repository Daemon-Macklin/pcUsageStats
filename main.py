#!/usr/bin/python3
# Main Script Controllign program


from influxdb import InfluxDBClient
import psutil
import time
import json
import datetime


# Method to control what happens
def main():
	print("Main Process")
	data = {}

	# For ever
	while(1):

		# Try to get the data
		try:
			data = gatherData()
		except Exception as e:
			print(e)	
		
		# Try to insert the data
		try:
			dbInsert(data)
		except Exception as e:
			print(e)

		# Wait 5 seconds
		time.sleep(5)

# Method to gather data
def gatherData():

	
	print("Gathering Data")
	data = {}
	
	# Get the data
	cpuPer = psutil.cpu_percent(interval=1)
	virMem = psutil.virtual_memory()
	swapMem = psutil.swap_memory()
	
	# Extract data
	data = {
		"cpuPer" : cpuPer,
		"virMemPer" : virMem.percent,
		"virMemUsed" : virMem.used,
		"swapMemPer" : swapMem.percent,
		"swapMemUsed" : swapMem.used
	}
	
	# Return data
	return data
	

# Method to insert the data
def dbInsert(data):
	print("Insert into db")
	
	# Connect to database
	client = InfluxDBClient(host ='localhost', port=8086, username='pcStatus', password='admin', database='pcUsageStats')
	
	# Create json object to insert
	json_body = [
		{
		"measurement" : "recordings",
		"tags": {
		"time" : datetime.datetime.utcnow().isoformat(),
			},
		"time": datetime.datetime.utcnow().isoformat(),
		"fields" : {
			}
		}
	]

	# Add data to object
	json_body[0]["fields"] = json.loads(json.dumps(data))
	print(json_body)
	
	# Insert object into db
	client.write_points(json_body)


main()
