#Log the pwd
	DIR="$(pwd)"

############Chauncey###############
# This section of logical statements is designed to kill the process if its not run somewhere its supposed to be run.
# Additionally, it cd's to the correct directory in the event of a cron job running in the root directory
# Please replace this logic with whatever makes sense for our architecture.
###################################

	# if [[ $DIR == '/home/ec2-user' ]]; then
	# 	echo "Script running on the EC2 instance"
	# 	cd work/egallon
	# elif [[ $DIR == '/Users/daniel.wood/Sites/egallon_data_processor' ]]; then
	# 	echo "Script Running Locally"	
	# 	cd /Users/daniel.wood/Sites/egallon_data_processor
	# else 
	# 	echo "Unsure where you're running this file, we're going to kill the process"
	# 	exit
	# fi

############################ End logic ###############################

RunUtilityProcess() {	
	echo
	echo 'Download and Process Utility Data and Push it the correct place'
	echo
	date
	echo

	python script.py 	
	# Need to push the data around here to the correct places
}

Diagnostic() {
	echo
	echo
	echo 'Diagnostic tests on the resulting data'
	date
	python diagnostic.py	
}

# Run the process and send the output to a log file. 
# RunUtilityProcess 2>&1 | tee -a output_archive.log 
RunUtilityProcess

# Clear the output.log
> output.log
Diagnostic 2>&1 | tee -a output.log | tee -a output_archive.log
Diagnostic

############Chauncey###############
# At this point, it would be great to send an email of output.log to daniel.wood@hq.doe.gov
###################################
