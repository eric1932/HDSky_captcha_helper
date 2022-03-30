# HDSky Captcha Helper
Use [Baidu OCR API](https://cloud.baidu.com/doc/OCR/index.html) to recognize verification code

Example:
![image](https://user-images.githubusercontent.com/10938293/160747970-51423778-d6bc-40f4-a17a-48451f3765c0.png) = `7D8DA7`

## Setup
You need to create `app/.env` and fill in credentials as described below
```
APP_ID=''
API_KEY=''
SECRET_KEY=''
```

Then, use `build.sh` and `run.sh` to deploy Docker image.

### Docker CLI
You may shadow .env file into `sysenv`
```
docker run -d \
  --name=HDSky_captcha_helper \
  -e APP_ID='app_id' \
  -e API_KEY='api_key' \
  -e SECRET_KEY='api_secret' \
  -p 80:80 \
  --restart unless-stopped \
  hdsky-captcha:latest
```

## Usage
GET API path `/hdsky/captcha/{image_hash}` and return will be like
```json
{
  "status": 0,
  "code": "RESULT_CODE"
}
```

## TODOs
✅ Update Dockerfile to take `.env` vars
