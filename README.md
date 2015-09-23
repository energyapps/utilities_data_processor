# egallon_data_processor

The directory structure should look like this:
Root
- script.py <--this compiles the data from EIA, and saves it to directories (below)
- diagnostic.py <--error handling and checking to ensure that everything works, and give averages of values
- oil_meta.json <--meta data to append to oil data that is downloaded
- electricity_meta.json <--meta data to append to electricity data that is downloaded
- egallon.sh <-- artifact, but could possess the code for what is run in the jenkins job.
- output_archive.log <-- compiled outputs from each egallon.sh run.

Every time the jenkins job runs, the following files will be generated and synced to where they can be accessed by ajax call. 
- electricity/elweeklyarchive-DD-MM-YY.json <--weekly json download of historical data for archive
- current/el.json <-- Paired down version of the above for only this week (overwritten each time)
- oil/oilweeklyarchive-DD-MM-YY.json <--weekly json download of historical data for archive
- current/oil.json <-- Paired down version of the above for only this week (overwritten each time)
- current/combined.json <-- oil.json and el.json combined. (overwritten each time) ONLY FILE THAT NEEDS TO BE SERVED FOR LIVE GRAPHIC
- output.log <-- any errors and some statistics from most recent egallon.sh run. (overwritten each time) emailed to Daniel Wood
