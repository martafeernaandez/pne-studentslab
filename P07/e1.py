import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS = '?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS

print(f"Server: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", ENDPOINT + PARAMS)

    response = conn.getresponse()
    print(f"Response received!: {response.status} {response.reason}")
    print()

    data = response.read().decode("utf-8")

    json_response = json.loads(data)

    if 'ping' in json_response and json_response['ping'] == 1:
        print("PING OK! The database is running!")
    else:
        print("Ping failed or unexpected response format.")

except Exception as e:
    print(f"An error occurred during the connection: {e}")
finally:
    conn.close()