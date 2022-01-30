import re

from fastapi import FastAPI

import hdsky

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


@app.get("/hdsky/captcha/{image_hash}")
def hdsky_captcha(image_hash: str):
    # check hash (eg. 2f92cc2f6184b147fed10433d6b64e57)
    # 91b2162cc946786a19a1c4659706159f = 6BB372
    if not re.match(r"[a-z0-9]{32}", image_hash):
        return {"status": 1, "message": "invalid hash"}
    full_url = f"https://hdsky.me/image.php?action=regimage&imagehash={image_hash}"
    result_code = ""
    for i in range(hdsky.MAX_RETRY):
        result_code = hdsky.recognize(full_url)
        if re.match(r"[A-Z0-9]{6}", result_code):
            break
    print(f"Result: {image_hash}/{result_code}")
    return {"status": 0, "code": result_code}
