# bosch-line-detection

bosch-line-detection packages a machine learning model that is used to detect auto failure according to data collected from auto-line detection.

This web application enables users to upload a file, use the uploaded file to do the training and prediction. 

## Deploy the application
In the folder of bosch-line-detection, you may run the following script to build a file, e.g., line_detector-1.0.0-py3-none-any.whl

```bash
python3 setup.py bdist_wheel
``` 
You may copy the `.whl` file and `deploy.sh` to the target folder and target machine. Then deploy to `waitress-serve` by:
```bash
sh deploy.sh
``` 
You may deploy to other cloud or local service.

In case you want to run locally with a development mode, please do:

```bash
echo "create a virtual environment"
python3 -m venv venv
. venv/bin/activate

export FLASK_APP=line_detector
set FLASK_ENV=development
flask init-db
flask run

``` 

## User guide
Use a browser to `http://localhost:8080` , which opens the welcome page.

### Welcome page
The welcome page leads you to: upload a file, training, and prediction.

### upload a file
You may upload a file with csv or zip version.
Please note that the file name cannot be duplicated, please rename, e.g., add trailing date, as required 
You can also use endpoint `/upload` post method by specifying the file.
The api will automatically detect the file extension and will give warning message if uploading is failed

### training
Please upload a file first and then use the filename to do the training.
You may use the UI training page, or use `/train` post method with `training_file` or `/train/<training_file>`

### prediction
Please upload a file first and then use the filename to do the prediction.
You may use the UI training page, or use `/predict` post method with `prediction_file` or `/predict/<prediction_file>`

## Version Release
bosch-line-detection v1.0.0

## Proposals for future version
### Data architecture
When we have the chance of putting this api in cloud, we may :

* Use a cloud file system, e.g., s3, to save the uploaded files and each version of models
* Separate the training and prediction process. 
    * When there is a training process, the prediction continues to use the old version of model.
    * When a new version of model is generated and saved to s3, set up a notice, so that the web application will update its model from s3.
* API cache: 
    * To release the burden of api which may do prediction of a used uploaded file, we may set up a cache to cache the result of prediction.
    * This cache should be cleaned whenever there is a new model generated after the training process
    * We may discuss if using that `files` table in db to avoid using a training file twice.  
 
 