#!/usr/bin/env python

#Calculates the Mean Average Precision, as in: http://www.kaggle.com/c/FacebookRecruiting/details/Evaluation

import csv
import sys

def MeanAveragePrecision(valid_filename, attempt_filename, at=10):
    at = int(at)
    valid = dict()
    for line in csv.DictReader(open(valid_filename, 'r')):
        valid.setdefault(line['source_node'], set()).update(line['destination_nodes'].split(" "))

    attempt = list()
    for line in csv.DictReader(open(attempt_filename, 'r')):
        attempt.append([line['source_node'], line['destination_nodes'].split(" ")])

    average_precisions = list()
    for entry in attempt:
        node = entry[0]
        predictions = entry[1]
        correct = list(valid.get(node, dict()))
        total_correct = len(correct)
        if len(predictions) == 0 or total_correct == 0:
            average_precisions.append(0)
            continue
        running_correct_count = 0
        running_score = 0
        for i in range(min(len(predictions), at)):
            if predictions[i] in correct:
                correct.remove(predictions[i])
                running_correct_count += 1
                running_score += float(running_correct_count) / (i+1)

        average_precisions.append(running_score / min(total_correct, at))

    return sum(average_precisions) / len(average_precisions)
