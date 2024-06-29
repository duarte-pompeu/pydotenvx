# pydotenvx

## Requirements

- [Poetry](https://python-poetry.org/docs/#installation)
- [Pyenv](https://github.com/pyenv/pyenv#installation)

## Installing

Run the following to configure `poetry`  and `pyenv`:

```bash
bash setup.sh
```

## Configuration

Populate `env/app.env` for your configuration. An example is available at `env/example.env`.

`env/app.env` is not version controlled because this:

- lets different people to use different configs
- avoids exposing sensible configurations, eg passwords

## Running the application

```bash
make run
```

You can now access a local webserver example at http://localhost:8000.

## Running with docker

```bash
docker compose up
```

You can now access a containerized webserver example at http://localhost:8000.

## Running with kubernetes

```bash
docker build --tag "docker.io/library/pydotenvx:latest" .
kubectl apply --filename kubernetes/
```

If you want to see the results, you can use port-forwarding:

```
kubectl port-forward services/pydotenvx-service 8000:80
```

And now you can validate your orchestration at http://localhost:8000.

--

Based on [my-python-template](https://github.com/duarte-pompeu/my-python-template), created by [Duarte Pompeu](https://duartepompeu.com).