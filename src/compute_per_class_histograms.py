import argparse
import matplotlib.pyplot as plt
import operator
import os
from operator import itemgetter
import pandas as pd
import seaborn as sns
import sklearn
import sys


# Seaborn settings.
sns.set_style('white')
sns.set_context('paper', font_scale=2, rc={'lines.linewidth': 3})
sns.despine(left=True, bottom=True)


def plot_histogram(df, out_pdf, x_axis_label, y_axis_label, min_x, max_x,
        normalize_counts=False):
    plt.figure()

    # FIXME: revisit, as what we want here is a "relative histogram" instead.
    ax = sns.distplot(df, norm_hist=normalize_counts)
    ax.set(xlabel=x_axis_label, ylabel=y_axis_label, xlim=(min_x, max_x))

    fig = ax.get_figure()
    fig.set_size_inches(6.5, 4)
    fig.savefig(out_pdf, format='pdf', bbox_inches='tight')

    print 'Saved histogram as "%s".' % out_pdf


def build_per_class_histograms(input_file, class_number, output_dir,
        normalize_counts):
    # XXX: Assumes file is space separated file without header in the following
    # format:
    #
    # <image> <class_label> <prediction> <unit_0> <unit_1> ... <unit_n>
    df = pd.read_csv(input_file, sep=' ', header=None)
    non_unit_cols = ['image', 'class_label', 'top1_pred']
    colnames = ['unit_' + str(c - 3) for c in df.columns]
    for idx, c in enumerate(non_unit_cols):
        colnames[idx] = c

    df.columns = colnames

    # As per above, first 3 columns are not units.
    count_units = len(colnames) - 3

    # Per class groups.
    count_hist = 0
    for idx, g in df.groupby(['class_label', 'top1_pred']):
        class_label = idx[0]
        pred = idx[1]

        if class_label != class_number:
            continue

        is_misclassified = class_label != pred
        out_pdf = output_dir + '/class_' + str(class_label)
        out_pdf += '_misclassified_as_' + str(pred) if is_misclassified else ''
        out_pdf += '-' + str(len(g)) + '_examples'
        out_pdf += '.pdf'

        # FIXME: Raw data is coming in as averages though, so need to ask Matt
        # for raw sums instead.
        hist_df = g.drop(non_unit_cols, axis=1).sum()
        plot_histogram(hist_df, out_pdf, 'Unit',
                       'Sum of activations', min_x=0,
                       max_x=count_units, normalize_counts=True)

        count_hist += 1

    if count_hist == 0:
        print 'No histograms computed for class %s' % class_number


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Outputs per class histograms.')
    parser.add_argument('-i', '--input_file',
                        help='Relative path of input file with raw data.',
                        required=True)
    parser.add_argument('-c', '--class_number',
                        help='Class number for which to compute histograms.',
                        type=int,
                        required=True)
    parser.add_argument('-o', '--output_dir',
                        required=True)
    parser.add_argument('--normalize_counts',
                        help='Normalize counts for each histogram bar, '
                        'effectively plotting what is know as a "relative '
                        'histogram".',
                        dest='normalize_counts',
                        action='store_true')
    parser.set_defaults(normalize_counts=False)

    args = parser.parse_args()
    build_per_class_histograms(**vars(args))
