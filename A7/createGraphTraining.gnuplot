set term png
set datafile separator ","
set output "plot_training.png"
set xlabel "Training set size"
set ylabel "% accuracy"
plot "perceptron_valid.csv" using 1:2 title "Validation accuracy" with lines, \
 "perceptron_test.csv" using 1:2 title "Test accuracy" with lines
