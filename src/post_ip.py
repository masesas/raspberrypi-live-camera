import requests
import re


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def read_ngrok_log():
    """read_ngrok_log
    read from log file and the ngrok url
    """

    with open("/home/pi/ngrok.log", "r") as file_input:
        list_lines = file_input.readlines()
        for line in list_lines:
            # print("the line", line)
            x = re.search(".*url=(tcp://.*)", line)
            try:
                return x.group(1)
            except:
                continue


def get_and_post_ip():
    # khesa token. please create your own in ngrok.com > dashboard.ngrok.com > API
    my_token = "2gSpPUzhnowwp4AdDtVFige0jgH_nPD8K5vhEWVb3MDKgaAq"
    endpoint = "https://api.ngrok.com/endpoints"
    headers = {"Ngrok-Version": "2"}
    get_ngrok = requests.get(headers=headers, url=endpoint, auth=BearerAuth(my_token))
    response = get_ngrok.json()

    public_ip = None
    for data in response["endpoints"]:
        if data["proto"] == "https":
            public_ip = data["public_url"]
            break

    print(f"public ip={public_ip}")

    if public_ip != None:
        post_device_ip = requests.post(
            f"http://103.190.28.211:3000/api/v1/camera",
            json={"vehicle_id": "1HBGH1J787E", "ip_address": f"{public_ip}:"},
        )

        print(f"post_device_ip={post_device_ip.status_code}")
    else:
        print("failed to get and post public ip")

