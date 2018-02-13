#################################################################
#################################################################
############### Normalize Dataset
#################################################################
#################################################################

#############################################
########## 1. Load libraries
#############################################
##### 1. General support #####
import scipy.stats as ss
import numpy as np
import warnings
import os
from rpy2.robjects import r, pandas2ri
pandas2ri.activate()

##### 2. R #####
r.source(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'R', 'normalize.R'))

#######################################################
#######################################################
########## S1. Dataset Normalization
#######################################################
#######################################################

#############################################
########## 1. Z-score
#############################################

def zscore(dataset, normalization='rawdata', normalize_cols=True, log=True):

	# Get raw data
	rawdata = dataset[normalization]

	# Z-score without warnings
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		if normalize_cols:
			rawdata = rawdata/rawdata.sum()
		if log:
			rawdata = np.log10(rawdata+1)
		zscore = rawdata.apply(ss.zscore, axis=1).dropna()

	# Return
	return zscore

#############################################
########## 2. VST
#############################################

def vst(dataset):

	return pandas2ri.ri2py(r.vst(pandas2ri.py2ri(dataset['rawdata'])))

#############################################
########## 3. Quantile Normalization
#############################################

def quantile(dataset):

	return pandas2ri.ri2py(r.quantile(pandas2ri.py2ri(dataset['rawdata']))).set_index('gene_symbol')

#############################################
########## 4. Combat
#############################################

def combat(dataset, batch_column='batch', covariates=[], normalization='rawdata'):

	# Get covariate formula
	covariate_formula = '~'+'+'.join(covariates) if len(covariates) else np.nan

	# Filter variable genes
	gene_var = dataset[normalization].var(axis=1)
	data = dataset[normalization].loc[gene_var[gene_var > 0].index]

	return pandas2ri.ri2py(r.combat(pandas2ri.py2ri(data), pandas2ri.py2ri(dataset['sample_metadata']), batch_column, covariate_formula))
