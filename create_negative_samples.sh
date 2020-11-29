for filename in $(ls negatives/hats/)
do
    echo "negatives/hats/"$filename >> "negatives.txt"
done;

for filename in $(ls negatives/kaggle_backgrounds/)
do
    echo "negatives/kaggle_backgrounds/$filename" >> "negatives.txt"
done;