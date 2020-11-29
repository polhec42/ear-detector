positive_samples="ears_positive_samples.vec"
negative_samples="negatives.txt"
num_positives=1500
num_negatives=3000
num_stages=20
width=16
height=32
type="LBP"

opencv_traincascade -data classifier -vec $positive_samples -bg $negative_samples -numPos $num_positives -numNeg $num_negatives -numStages $num_stages -w $width -h $height -featureType $type