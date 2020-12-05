# ear-detector

This repository contains all code that was written for an ear detector. Train datasets are not included.

In order to re-run the evaluation stage, run the `rerun.sh`. This script will remove the previous evaluation and will evaluate the whole test dataset and save the images of the detections together with `results.csv` file that contains number of TP, FP and TN for every image and overall acurracy on the test dataset.

## Directory structure

### classifier
Folder `classifier` contains `cascade.xml` of the best trained model and folders of 4 different classifiers that were trained on different dataset. Each of that folders containts all files (except for images) that is needed to train the model again and get the same results.

### figures
Folder `figures` contains results (in the form of `.csv` file) of different models on the test dataset that was used to draw some plots. Folder also contains some plots that were used for the report.

### .

This directory contains many files that were used for training. Some of those files are only simple .sh scripts that make the training easier.

#### shell scripts
Each script has descriptive name and it does one step of the training procedure:
* `create_negative_samples.sh`: it gets the file names of the negatives and writes them in file negatives.txt which is an input to the `opencv_traincascade` command.
* `create_positive_samples.sh`: it runs the opencv_createsamples command using the preprocessed data and creates the binary `.vec` file which is one of the inputs to the `opencv_traincascade` command.
* `train_cascade.sh`: it binds the list of variables to the parameters of `opencv_traincascade` command and runs the training stage. It's purpose is easier parameter handling.

#### python files
Each python file has descriptive name:
* `data_preprocessing.py`: creates .info file which tells the opencv where are the bounding boxes of the ears in the positive images.
* `get_negative_samples.py`: simple python program that downloads the images of the people with the swimming hat from the ImageNet. After that it is required to manually postprocces those files, as are some corrupted.
* `performance.py`: this python program evaluates the ear detector (it's `cascade.xml` has to be in the `classifier` directory) on different set of detector parameters (scale and minNeighbors) and writes the results in `configurations.csv`.
* `rectangle.py`: utility class for Rectangles which was used in the data preprocessing stage and evaluation steps for extracting bounding boxes from the segmented ears.
* `store_masks.py`: runs the bounding box algorithm on the test dataset and writes the locations and sizes of the rectangles in the `test_rectangles.csv` file. This was done of-line in order to speed up the evaluation step. The `performance.py` script has to only load those masks and doesn't have to extract them each time seperately, which is very time consuming.
* `detector.py`: the actual detector that runs the ear detector (it's `cascade.xml` file has to be in `classifier` folder). It has 3 different modes:
    * detect mode: accepts the image, runs the ear detector and shows the resulting image with the marked ears.
    * classify mode: accpets the image and the reference, runs the ear detector, shows the resulting image with the marked ears and writes the locations of the detected ear together with the evaluation on the standard output.
    * classify-all mode: it accepts the folder that contains the test dataset. Then it runs the detector and stores both marked images and the evaluation result in the separate `results.csv` file in the `classifier/evaluation` folder. This can be extremly useful in the analysis step.
