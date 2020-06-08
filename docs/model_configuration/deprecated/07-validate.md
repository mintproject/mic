It's time to run and validate your component.

If you don't want to test the Docker Image, add the option `--no-docker`

```bash
$ mic model_configuration validate hello_world --no-docker
```

The validation process is going to validate:
- Pass the parameters to your model
- The execution on your machine
- The creation of the Docker Image
- The execution on your machine using Docker

```bash
$ mic model_configuration validate hello_world/
[OK] Parameters
[OK] Execution without Docker
[OK] Extraction of dependencies
[OK] Build Docker Image
[OK] Execution using Docker

Created: hello_world/hello_world.zip
```

The result is going to be a zip file.