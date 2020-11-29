positive_samples="ears_positive_samples.vec"
negative_samples="negatives.txt"
num_positives=650
num_negatives=1400
num_stages=19
width=15
height=30
type="LBP"

opencv_traincascade -data classifier -vec $positive_samples -bg $negative_samples -numPos $num_positives -numNeg $num_negatives -numStages $num_stages -w $width -h $height -featureType $type