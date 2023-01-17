import json


def get_port_number() -> int:
    port = 9000
    try:
        f = open('./vrc-discord-osc.config.json')
        data = json.load(f)
        f.close()
        if ("port" in data):
            if type(data['port']) is int:
                print(f"Using port {data['port']}.")
                port = data['port']
    except:
        print("Config file not found...")
    finally:
        if port == 9000:
            print("Defaulting to port 9000.")
        return port
