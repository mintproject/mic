## Identify the output files

Now, we must identify the outputs of your model.

!!! question
    Why is it important?
    You can add metadata about the outputs such as Units, formats, etc.

The output of your models are in the directory src/

Let's suppose that the output files are the file `file.txt` and the directory `src/images`

You must run:

```bash
$ mic modelconfiguration outputs src/file.txt src/images
```

Then, the config file `config.yaml` has been updated

```yaml
inputs:
    - name: gldas_noaho25_m.2.1
      path: data/GLDAS_NOAH025_M.2.1/
    - name:  
      path: data/prepicipitation_rates.txt
parameters:
    - name: start_date
      default_value: 2010
    - name: end_date
      default_value: 2012
outputs:
    - name: output_file
      path: src/file.txt
    - name: output_images
      path: src/images
```

Don't edit the outputs section manually!

!!! warning
    - If you edit the inputs or the parameters section in the `config.yaml` file. You must return to the [steop]

