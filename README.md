# Ypovoli

![backend linting](https://github.com/SELab-2/UGent-7/actions/workflows/backend-linting.yaml/badge.svg)
![backend tests](https://github.com/SELab-2/UGent-7/actions/workflows/backend-tests.yaml/badge.svg)

This application was developed within the framework of the course "Software Engineering Lab 2" within the Computer Science program at Ghent University.

## Documentation

See our wiki at [https://github.com/SELab-2/UGent-7/wiki](https://github.com/SELab-2/UGent-7/wiki) for more detailed information on the project's architecture.

A shorter summary for building the project locally can be found here:
- Run `development.sh`.
    - It starts the development environment and attaches itself to the output of the backend. The backend will auto reload when changing a file.
- Access the server by going to `https://localhost/api` for the backend and `https://localhost` for the frontend.
- If you change something to one of the docker files run `docker-compose -f development.yml up --build` to rebuild.
