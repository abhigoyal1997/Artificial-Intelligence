#!/bin/bash
rm perceptron_valid.csv perceptron_test.csv
for i in {1..10}
do
	num=`expr 100 \* $i`
	python dataClassifier.py -c perceptron -t $num
done