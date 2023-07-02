<a name="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Hack4change-inBin/Leaf-API">
    <img src="" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Leaf API</h3>

  <p align="center">
    Central API for all leaf front app and dashboards
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#image-processing">Image processing</a></li>
        <ul>
            <li><a href="#example">Example</a></li>
        </ul>
    <li><a href="#twelve-factor-app">Twelve-Factor App</a></li>
    <li><a href="#openapi">OpenAPI</a></li>
    <li><a href="#contact">Contact</a></li>

  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project
<p align="right">(<a href="#">back to top</a>)</p>

### Built With

* [![Nginx][Nginx-icon]][Nginx-url]
* [![FastAPI][FastAPI-icon]][FastAPI-url]
* [![Kubernetes][Kubernetes-icon]][Kubernetes-url]
* [![Docker][Docker-icon]][Docker-url]
* [![Postgresql][Postgresql-icon]][Postgresql-url]
* [![Redis][Redis-icon]][Redis-url]




<p align="right">(<a href="#">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

This is an example of how to set up project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* docker

Before, approach you have to install docker and docker compose for your platform.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Hack4change-inBin/Leaf-API
   ```

2. Create backend.env files. You can just copy template, but changes are recommended
   ```sh
   cp env/examples/backend.env.example env/backend.env
   ```

3. Create db.env files. You can just copy template, but changes are recommended
   ```sh
   cp env/examples/db.env.example env/db.env
   ```

4. Build docker containers
   ```sh
   docker-compose build
   ```

5. Run containers
   ```sh
   docker-compose up
   ```

<p align="right">(<a href="#">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Dev tools config (tests, linter, formatting, etc.)
- [x] Ci integration using pre-commit
- [x] JWT auth
- [x] Celery queue system integration
- [x] Image processing
- [ ] Permissions system (in progress)
- [ ] API for social side
- [ ] API for business side
- [ ] Redis Cache
- [ ] Nginx config
- [ ] Kubernetes config

<p align="right">(<a href="#">back to top</a>)</p>

## Image processing

When user uploading and image to API, Celery workers process image to different sizes
You can configure sizes which you want use using `AVAILABLE_IMAGE_SIZES` env variable (separated with comma)
and then specify width and height of the size by declaring variable `{SIZE_NAME}_IMAGE_SIZE={WIDTH}x{HEIGHT}`.
In local environment You can find it in `env/backend.env` file.
To request of the image set `image-size` header with value which you define before in `env/backend.env`

### Example:

Sizes:

* small - 480p
* medium - 720p
* large - 1080p

Variables:

* `SMALL_IMAGE_SIZE=854x480`
* `MEDIUM_IMAGE_SIZE=1280x720`
* `LARGE_IMAGE_SIZE=1920x1080`

Request Headers:

* small - `image-size=small`
* medium - `image-size=medium`
* large - `image-size=large`

## Twelve-Factor App

Leaf Backend meet requirements of Twelve-Factory App methodology

The Twelve-Factor App is a methodology for building modern, cloud-native software-as-a-service (SaaS) applications.
It provides a set of best practices to ensure scalability, maintainability,
and portability of applications in cloud environments.
The Twelve-Factor principles were introduced by Heroku, a popular cloud platform,
and have been widely adopted in the industry.

### Benefits of the Twelve-Factor App Approach
* Simplifies deployment and scaling of applications in cloud environments.

* Enhances portability and allows for easy migration across different platforms and providers.

* Facilitates team collaboration by providing a set of shared best practices.

* Improves maintainability and robustness through the use of stateless processes and externalized configuration.

* Enables efficient development, testing, and debugging by adhering to consistent and isolated environments.


## OpenAPI

Leaf API use OpenAPI 3.0. If you already have project up and running on you local environment,
you can open built in swagger on `http://localhost:8000/docs`. To import open api schema go to
`http://localhost:8000/openapi.json`


<!-- CONTACT -->

## Contact

Grzegorze Pisarczyk - [@linkedin_handle](https://www.linkedin.com/in/grzegorz-pisarczyk) - qtquicksoft@gmail.com

Maciej Żuk - [@linkedin_handle](https://www.linkedin.com/in/maciej-%C5%BCuk-111138214/) - maciekzuk4@icloud.com

Mateusz Borucki - mateuszborucki1@gmail.com

Roland Sobczak - [@linkedin_handle](https://www.linkedin.com/in/roland-sobczak/) - rolandsobczak@icloud.com


Project Link: [https://github.com/Hack4change-inBin/Leaf-API](https://github.com/Hack4change-inBin/Leaf-API)

<p align="right">(<a href="#">back to top</a>)</p>


<p align="right">(<a href="#">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB

[React-url]: https://reactjs.org/

[Nginx-icon]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white

[Nginx-url]: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwj_tPvV4Mn_AhXY6CoKHZ92BNYQFnoECA4QAQ&url=https%3A%2F%2Fwww.nginx.com%2F&usg=AOvVaw10RW2cXcmCuZ2YnsYWHFKR&opi=89978449

[FastAPI-icon]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[FastAPI-url]: https://fastapi.tiangolo.com

[Kubernetes-icon]: https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white

[Kubernetes-url]: https://kubernetes.io

[Docker-icon]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[Postgresql-icon]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white

[Postgresql-url]: https://www.postgresql.org

[Redis-icon]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white

[Redis-url]: https://redis.io
