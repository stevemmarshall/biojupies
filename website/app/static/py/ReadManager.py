#################################################################
#################################################################
############### Table Manager API ###############################
#################################################################
#################################################################
##### Author: Denis Torre
##### Affiliation: Ma'ayan Laboratory,
##### Icahn School of Medicine at Mount Sinai

#################################################################
#################################################################
############### 1. Library Configuration ########################
#################################################################
#################################################################

#############################################
########## 1. Load libraries
#############################################
##### 1. Python modules #####
import json
import urllib.request
import pandas as pd
from io import StringIO

#############################################
########## 2. Variables
#############################################

#################################################################
#################################################################
############### 1. Expression Table #############################
#################################################################
#################################################################

#############################################
########## 1. Merge counts
#############################################

def mergeCounts(alignment_uid):

	# Get samples
	req =  urllib.request.Request('https://amp.pharm.mssm.edu/charon/files?username={ELYSIUM_USERNAME}&password={ELYSIUM_PASSWORD}'.format(**os.environ))
	uploaded_files = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))['filenames']
	samples = [x for x in uploaded_files if x.startswith(alignment_uid) and x.endswith('_gene.tsv')]

	# Initialize dict
	results = []

	# Read
	for sample in samples:

		# Get sample name
		sample_name = sample[len(alignment_uid)+1:-len('_gene.tsv')]

		# Get counts from S3
		req =  urllib.request.Request('https://s3.amazonaws.com/biodos/c095573dc866f2db2cd39862ad89f074/'+sample)

		# Build dataframe
		counts = pd.read_table(StringIO(urllib.request.urlopen(req).read().decode('utf-8')), header=None, names=['gene_symbol', 'counts'])
		counts['counts'] = counts['counts'].astype(int)
		counts['sample'] = sample_name
		
		# Append
		results.append(counts)

	# Create dataframe
	count_dataframe = pd.concat(results).pivot_table(index='gene_symbol', columns='sample', values='counts')

	# Return
	return count_dataframe#json.dumps(count_dataframe.to_dict(orient='split'))


#############################################
########## 1. Upload UID
#############################################

def uploadToDatabase(upload_uid, samples, session, tables):

	# Fetch ID
	query = session.query(tables['fastq_upload'].columns['id']).filter(tables['fastq_upload'].columns['upload_uid'] == upload_uid).all()
		
	# Try
	try:

		# If query is empty
		if len(query) == 0:

			# Upload and get ID
			upload_id = session.execute(tables['fastq_upload'].insert().values([{'upload_uid': upload_uid}])).lastrowid
			
			# Upload samples
			session.execute(tables['fastq_file'].insert().values([{'filename': sample[12:], 'fastq_upload_fk': upload_id} for sample in samples]))

		# Close session
		session.commit()

	except:

		session.rollback()

	session.close()


#############################################
########## 1. Upload UID
#############################################

def uploadJob(jobs, session, tables):

	# Get first job
	job = jobs[0]['outname']
	paired = jobs[0]['datalink'].count('https://s3.amazonaws.com/biodos') > 1

	# Get UIDs
	alignment_uid, upload_uid, sample = job.split('-', 2)
	species = sample.split('-')[-1]

	# Add new alignment job with UID, upload FK, and organism
	query = session.query(tables['fastq_alignment'].columns['id']).filter(tables['fastq_alignment'].columns['alignment_uid'] == alignment_uid).all()

	try:

		# If query is empty
		if len(query) == 0:

			# Get ID
			upload_id = session.query(tables['fastq_upload'].columns['id']).filter(tables['fastq_upload'].columns['upload_uid'] == upload_uid).all()[0][0]
			
			# Upload samples
			session.execute(tables['fastq_alignment'].insert().values([{'alignment_uid': alignment_uid, 'fastq_upload_fk': upload_id, 'species': species, 'paired': paired}]))

		# Close session
		session.commit()

	except:

		session.rollback()

	session.close()
