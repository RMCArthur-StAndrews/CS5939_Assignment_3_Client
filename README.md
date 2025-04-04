# READ ME 
This aspect of the project covers modules: 

 - The Edge API 
 - The Edge Client (Web App)
 
 ## Running on Local Machine
Prior to running this service on your local machine, please make sure that localhost:4000 is available. Failure to have this port available will result in a failure of service. This is to ensure that the Edge API is in the correct communication point to interact with the web client. The Edge Client, however, does not need to be on a specific port.

### Running the Edge Client 
Prior to running locally, ensure that you have Node.js (and by extension npm) present on your machine. 
To run the edge client, open a terminal via your machine or chosen IDE which can support npm queries. Direct the terminal to the edge-client folder, as shown below:

    cd edge-client
 Next, run a clean build of the project with the following command: 
 

    npm run build
 
 Should there be no adjustments needed, you can then run the webapp by running the following command:
 

    npm run start 
Once the service is running, you should see in the console a locally hosted site you can reach to view the web application. Depending on your machine's permissions, a browser may pop up with the web app loaded.

### Run the Edge API 
To run the service on your local machine without containers, you should *ensure that you have Python 3.11 installed on your machine as a minimum*.
    

## Running on Containers
If running the service on a container, you will not need to consider which ports are available as it is expected that the container should have those ports available. 
