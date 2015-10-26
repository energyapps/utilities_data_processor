# utilites_data_processor

Scrape and compile monthly EIA residential utility price data: http://www.eia.gov/electricity/monthly/epm_table_grapher.cfm?t=epmt_5_06_a

The directory structure should look like this:
Root
- script.py <--this compiles the data from EIA, and saves it to directories (below)
- diagnostic.py <--error handling and checking to ensure that everything works, and give averages of values
- electricity_meta.json <--meta data to append to electricity data that is downloaded
- utility.sh <-- artifact, but could possess the code for what is run in the jenkins job.
- output_archive.log <-- compiled outputs from each egallon.sh run.

Every time the jenkins job runs, the following files will be generated and synced to where they can be accessed by ajax call. 
- electric_utilities_monthly.json <--- Monthly EIA utilities data, state by state
- output.log <-- any errors and some statistics from most recent egallon.sh run. (overwritten each time) emailed to Daniel Wood
