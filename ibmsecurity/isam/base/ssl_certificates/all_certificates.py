import logging
import os.path
import json

logger = logging.getLogger(__name__)

uri = "/isam/ssl_certificates"



def get_all_certificates (isamAppliance, check_mode=False, force=False):
	"""
	Get information about all certificates on the appliance	
	"""
	import time
	epoch_time = int(time.time())
	
	certs=[]
	dbs_obj = isamAppliance.invoke_get("Retrieve all certificate databases", uri)
	dbs=dbs_obj['data']
	for db in dbs:
		pcert_obj=isamAppliance.invoke_get("Retrieve personal certificates", "{0}/{1}/personal_cert".format(uri,db['id']))
		logger.info("Got object {0}".format(pcert_obj))
		pcerts=pcert_obj['data']
		for pcert in pcerts:
			cert_epoch = int(pcert['notafter_epoch'])
			certs.append({
						"db_id":db['id'],
						"cert_id":pcert['id'],
						"issuer":pcert['issuer'],
						"subject":pcert['subject'],						
						"type":"personal",
						"exp_epoch":pcert['notafter_epoch'],
						"exp_date":pcert['notafter'],
						"expired":cert_epoch < epoch_time
						})

		scert_obj=isamAppliance.invoke_get("Retrieve signer certificates", "{0}/{1}/signer_cert".format(uri,db['id']))
		scerts=scert_obj['data']
		for scert in scerts:
			cert_epoch = int(scert['notafter_epoch'])
			certs.append({
						"db_id":db['id'],
						"cert_id":scert['id'],
						"issuer":scert['issuer'],						
						"subject":scert['subject'],
						"type":"signer",
						"exp_epoch":scert['notafter_epoch'],
						"exp_date":scert['notafter'],
						"expired":cert_epoch < epoch_time})

		
	return_obj = isamAppliance.create_return_object()
	return_obj['data'] = certs
	
	return return_obj