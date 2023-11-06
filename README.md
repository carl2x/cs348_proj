# TodoHub
A TODO tracking webapp with tags, priority, and duration.

## Requirements
```
python >= 3.11
```

## Getting started
```bash
git clone https://github.com/carl2x/cs348_proj.git
cd cs348_proj
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP = app
flask run
```

## Setting up MySQL
Create a `app.yaml` file in the root folder with the following content:
```yaml
runtime: python311 # or another supported version

instance_class: F1 # GCP cheapest

# credentials
env_variables:
  MYSQL_USER: <user_name>
  MYSQL_PASSWORD: <user_password>
  MYSQL_DB: <database_name>
  MYSQL_HOST: <database_ip>

handlers:
# Matches requests to /images/... to files in static/images/...
- url: /img
  static_dir: static/img

- url: /script
  static_dir: static/script

- url: /styles
  static_dir: static/styles
```

## Reference
UI and Flask routing reference: https://tichung.com/blog/2021/20200323_flask/
