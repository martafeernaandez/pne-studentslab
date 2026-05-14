import http.client

SERVER = "localhost"
PORT = 8080


def request_endpoint(endpoint):
    print(f"\n--- Requesting: {endpoint} ---")
    conn = http.client.HTTPConnection(SERVER, PORT)
    try:
        conn.request("GET", endpoint)
        response = conn.getresponse()
        print(f"Status: {response.status}")

        data = response.read().decode("utf-8")
        print(f"Response length: {len(data)} characters")

        conn.close()
    except ConnectionRefusedError:
        print("Error: Ensure the server is running.")


if __name__ == "__main__":
    endpoints = [
        "/geneLookup?gene=FRAT1",
        "/geneSeq?gene=FRAT1",
        "/geneInfo?gene=FRAT1",
        "/geneCalc?gene=FRAT1",
        "/geneList?chromo=9&start=22125500&end=22136000"
    ]

    for ep in endpoints:
        request_endpoint(ep)