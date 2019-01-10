set term png
set datafile separator ","
set output "plot_iterations.png"
set xlabel "Number of data-points seen"
set ylabel "% Validation accuracy"
plot "perceptronIterations.csv" using 1:2 title "Validation accuracy versus number of data-points seen" with lines
