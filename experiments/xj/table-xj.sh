#!/usr/bin/sh

RES_TO_CSV=$ROOT/experiments/xj/resultsToCSV.py
R_SCRIPT=$ROOT/experiments/xj/generateXJTable.r

TMP_DIR=/tmp/xj

rm -rf $TMP_DIR
mkdir  $TMP_DIR

$RES_TO_CSV $RESULTS_DIR/xj/default/native-seqhashset     > $TMP_DIR/native.csv
$RES_TO_CSV $RESULTS_DIR/xj/default/native-closedhashset  > $TMP_DIR/native-xj.csv
$RES_TO_CSV $RESULTS_DIR/xj/default/crochet-seqhashset    > $TMP_DIR/crochet.csv
$RES_TO_CSV $RESULTS_DIR/xj/default/crochet-closedhashset > $TMP_DIR/crochet-xj.csv
$RES_TO_CSV $RESULTS_DIR/xj/default/xj-closedhashset      > $TMP_DIR/xj.csv

pushd $TMP_DIR
{
    #TODO Call R script to generate table
    Rscript $ROOT/experiments/xj/generateXJTable.r
}
popd

# rm -rf $TMP_DIR

