echo "Creating conda environment.."
conda create -p venv python==3.7 -y
echo "Conda environment created successfully."

echo "Activate conda environment."
conda activate consignment_pricing
echo "Environment Activated"

echo "Creating project structure."
mkdir application_logging app_exception consignment_data data logs notebooks reports source webapp
echo "Project structure created."

echo "started creating python script for each module.... :)"
touch app_eception/__init__.py app_exception/app_exception.py 
echo "app exception file created successfully."

echo "started creating python script for each module."
touch application_logging/__init__.py application_logging/logger.py 
echo "app logging file created successfully."

echo "Started creating pipeline scripts."
touch source/__init__.py source/data_preprocessing.py  source/feature_engineering.py source/get_data.py source/load_data.py source/split_data.py source/train_evaluate.py
echo "source script created."

echo "Started creating app logger scripts."
touch app_logger/__init__.py app_logger/logger.py
echo "App logger script created."

echo "Started creating requirements.txt file"
touch requirements.txt

echo "Started created setup.py file"
touch setup.py
echo "All required python scripts created successfully."

echo "Started created dvc.yaml file"
touch dvc.yaml
echo "dvc file created successfully."

echo "Started created params.yaml file"
touch params.yaml
echo "params file created successfully."