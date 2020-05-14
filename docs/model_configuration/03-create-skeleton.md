In this example, we are going to run a simple `python` code. 

```bash
$ python hello.py Fling output.txt
Created the file output.txt
```


This code creates the file `output.txt` 
```bash
Hello Fling!
```

The code is available [here](https://gist.github.com/dfc647d2cca69a8e9e7561aff668e2c3)

### Creating the directory skeleton for your first configuration

In this example, the command will be

```bash
$ mic model_configuration create_directory -n <model_name>
```

MIC has created a directory `model_name`.
In this directory, there two subdirectories:
- data: Contains your data/inputs.
- src: Contains the invocation script.