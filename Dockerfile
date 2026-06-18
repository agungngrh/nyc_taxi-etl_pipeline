# base image
FROM python:3.13-slim-bookworm

# set working directory
WORKDIR /app

# copy req.txt dan install dependency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy seluruh code project ke container
COPY . .

# permission execute ke shell script
RUN chmod +x scripts/entry_point.sh

# entry point program
CMD ["bash","./scripts/entry_point.sh"]