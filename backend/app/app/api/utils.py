import base64

def dict_to_b64(dict_in: dict) -> str:
    raw_data = "".join(
        [str(k) + str(v) for k, v in dict_in.items()]
    )

    return base64.b64encode(
        raw_data.encode('utf-8')
    ).decode('utf-8')
