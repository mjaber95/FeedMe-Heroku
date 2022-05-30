# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* TaxiFareModel/*.py

black:
	@black scripts/* TaxiFareModel/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr TaxiFareModel-*.dist-info
	@rm -fr TaxiFareModel.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

# ----------------------------------
#      VARIABLES
# ----------------------------------

# path to the file to upload to GCP (the path to the file should be absolute or should match the directory where the make command is ran)
# replace with your local path to the `train_1k.csv` and make sure to put the path between quotes


# bucket directory in which to store the uploaded file (`data` is an arbitrary name that we choose to use)
# name for the uploaded file inside of the bucket (we choose not to rename the file that we upload)


# project id - replace with your GCP project id

# bucket name - replace with your GCP bucket name


# choose your region from https://cloud.google.com/storage/docs/locations#available_locations

CONFIG = .env
include ${CONFIG}

run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}
	
yolo_train:
	@python train.py --img 640 --cfg YOLOv5_model/yolov5s.yaml --hyp YOLOv5_model/hyp.scratch.yaml --batch 32 --epochs 100 --data YOLOv5_model/model_data.yaml --weights yolov5s.pt --workers 24 --name yolo_road_det

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	#@gsutil cp train_1k.csv gs://wagon-data-847-jaber/data/train_1k.csv
	#@gsutil cp -r ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}
	@gsutil cp -r ${RECIPES} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}
	
upload_recipes_processed:
	@gsutil cp -r ${RECIPES_PROCESSED} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}
	
	
download_recipes:
	#@mkdir raw_data/Recipes
	@gsutil cp -r gs://${BUCKET_NAME}/${BUCKET_FOLDER}/raw_data/Recipes/ raw_data/

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER}  \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region ${REGION} \
		--stream-logs
		

download_model:
	@gsutil cp  gs://${BUCKET_NAME}/models/taxifare/model.joblib google_model.joblib

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)
