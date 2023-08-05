# Model Performance

# Introduction

This package calculates model performance metrics and confusion metrics at decile level of prediciton. Instead of calculating
the model performance at default probability cut-off of 0.5, this function divides prediction in 10 equal buckets and for each bucket
provides the model performance.

# Input

The function "conf_matrix" requires an input dataset name, the prediction feature name and the target feature name

# Results

decile_pred - Deciles of predictions.
cnt - Count of observations in each decile.
max_pred - Maximum probablity in each decile.
resp - Actual sum of target in each decile.
non_resp - Actual sum of non-target in each decile.
cumresp - Actual cumulative sum of target in each decile.
cumcnt - Cumulative count of observations in each decile.
resp_rate - Target rate of each decile.
lift - Lift in target rate of each decile. ex - By targeting top 20% customers we achieve 4x lift than random targeting.
tp - True positive at each decile cut-off.
fp - False positive at each decile cut-off.
tn - True negative at each decile cut-off.
fn - False negative at each decile cut-off.
precision - Precision at each decile cut-off.
recall - Recall at each decile cut-off.
fscore - Fscore at each decile cut-off.
ks - Maximum separation between target and non-target at each decile.

# Contact
Mrinal Shankar (https://github.com/mrinal-shankar)
 
