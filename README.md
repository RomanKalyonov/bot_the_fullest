# How to deploy:

1. Clone git project:

$ git clone git@github.com:semenovsd/bottemplate.git

2. Create .env file by the example.env in base folder

$ nano .env (ctrl+s - for save)

3. Run bash script for install and settings Docker:

$ sudo bash entrypoint.sh

4. Build up docker containers:
$ docker-compose up --build

Done!
