# kronobot

This repo contains all the code of the website from https://kronobot.com and the Telegram chatbot functionality
![kronobot.com preview](https://user-images.githubusercontent.com/17761956/205233198-f570797d-6c01-4233-835f-d731f5c3b696.png)
![Chatbot notification preview](https://user-images.githubusercontent.com/17761956/205232535-8c0943aa-6998-491c-bf1e-2101eb464425.jpeg)
![Chatbot chatroom preview](https://user-images.githubusercontent.com/17761956/205232603-bb1b26e8-dbb5-4b14-ba6e-af2d3df02bc2.jpeg)

### Development

Uses the default Django development server.

1. Check that you have your .env.dev and .env.dev.db.  If for some reason these files are not generated, remember that you can find samples in the repository.
   ```sh
   $ cat .env.dev
   
   DEBUG=1
   SECRET_KEY=zeBlas2JOF4PKSCX355yM6kT6WmMO24r
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=kronobot_dev
   SQL_USER=kronobot
   SQL_PASSWORD=dx!iT*YKan3CH6hBxet&6wRsl05Z
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   
   $ cat .env.dev.db

   POSTGRES_USER=kronobot
   POSTGRES_PASSWORD=dx!iT*YKan3CH6hBxet&6wRsl05Z
   POSTGRES_DB=kronobot_dev
    ```

2. Create docker volumes to save the data:
    ```sh
    $ docker volume create --name=kronobot_postgres_data_dev
    $ docker volume create --name=kronobot_grafana
    ```

3. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.
    Grafana dashboard will be accesible in [http://localhost:3000](http://localhost:3000).


### Deploying to production

You will have to configure the the Dockerhub account, the Github actions for the CI/CD, DNS and the production server:

* **Dockerhub:** You must create an [access token](https://docs.docker.com/docker-hub/access-tokens/) to download the Docker images from the production server. Then  you must create the following repositories in your Docker Hub account:
  * kronobot
  * kronobot-nginx
  * kronobot-prometheus


 * **Production server:** For this example we will be using [Digital Ocean](https://www.digitalocean.com/). Digital Ocean provides with droplets with Docker pre-installed. For an easy installation, I really recommend you to use those droplets. ![image](https://user-images.githubusercontent.com/17761956/140977706-ac9abf8f-931d-41e1-9908-218879b4b2b2.png)
   To deploy, you must create a deploy SSH key in your local machine that is going to be used to stablish connection between the CI/CD service and your production    server. The following command will create a **private** ssh key at **~/.ssh/id_deploy_rsa** and a **public** ssh key at **~/.ssh/id_deploy_rsa.pub**
   ```sh
   $ ssh-keygen -t rsa -C "your_email@example.com" -f ~/.ssh/id_deploy_rsa -N ''
   ```
   To let Github actions deploy to your production server, you must add the **id_deploy_rsa.pub** in the **~/.ssh/authorized_keys** file inside the production server.

    ```sh
    $ echo "ssh-rsa AAAACEzaC1yc2E...GvaQ your_email@example.com" >> ~/.ssh/authorized_keys
    ```

 * **Environment files:** Once the server is created, you must copy the .env files in the production server inside **/opt/kronobot** path.
    ```sh
    $ cat .env.prod
    $ cat .env.prod.db
    $ cat .env.prod.proxy-companion
    $ cat .env.prod.grafana
    ```

* **Github actions:** You must enable Github actions in your Github repository and add the required secrets inside Github
  * Push this repository to Github. 
  * Enable actions inside Repository > Settings > Actions > Actions permissions > Allow all actions.
  * Create the following secrets inside Repository > Settings > Secrets.
    * DOCKERHUB_USERNAME: Username of your Docker Hub.
    * DOCKERHUB_TOKEN: Access token generated previously in Docker Hub.
    * PRODUCTION_SERVER_USER: User used to connect to the production server via SSH.
    * PRODUCTION_SERVER_IP: Public IP of the production server.
    * SSH_PRIVATE_KEY: Generated deploy RSA private key (id_deploy_rsa).
    * SSH_PUBLIC_KEY: Generated deploy RSA public key (id_deploy_rsa.pub).

* DNS: It's important that the DNS records are setup properly before deploying the app to the production server. You will need to make sure that you have the following records:
  * A: record to set the IPv4 of your production server
  * AAAA: record to set the IPv6 of your production server
  * CNAME: record to configure the "wwww" subdomain.
  ![Screenshot from 2021-07-11 19-28-45](https://user-images.githubusercontent.com/17761956/125204570-40738000-e27e-11eb-81a4-7a495949af73.png)


# Hints to work with this project

1. To execute a command inside the Django container in **DEVELOPMENT** environment.
    ```sh
    $ docker-compose exec web python manage.py shell
    ```
2. To execute a command inside the Django container in **PRODUCTION** environment.
    ```sh
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py shell
    ```
3. To create Django migrations. In case you want to execute this in production environment, remember to use the -f parameter.
    ```sh
    $ docker-compose exec web python manage.py makemigrations
    ```
4. To execute Django migrations. In case you want to execute this in production environment, remember to use the -f parameter.
    ```sh
    $ docker-compose exec web python manage.py migrate
    ```
   
5. To create Django admin superuser. In case you want to execute this in production environment, remember to use the -f parameter.
    ```sh
    $ docker-compose exec web python manage.py createsuperuser
    ```
6. To configure the debugger in Pycharm you can use guide in the following [link](https://testdriven.io/blog/django-debugging-pycharm/#:~:text=To%20do%20so%2C%20open%20PyCharm,create%20a%20new%20Docker%20configuration.). Remember that you must have a professional license to use this feature.
