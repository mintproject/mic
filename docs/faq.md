
## Frequently Asked Questions

**What do the properties in the table mean?**

If you find any of the fields in the metadata table confusing, just select them for editing. You will be shown a definition of what each property means. For example by editing property 16 (Purpose):

```bash
Current value for Purpose is: ['Crop seasonal production']
Definition: Objective or main functionality that can be achieved by running this model
```

**I don't know all metadata of my model right now. Can I save my progress?**

Yes. You can use the `save` command at any point to save your progress. Your metadata will be saved as a JSON file, which you can load with the `load` command. When you are ready to submit, just type `send`.

**What happens if I submit my model metadata twice?** 

Right now MIC does not support editing model metadata. If you submit the same model metadata twice, you will create two entries in the catalog. We are working to support this feature.