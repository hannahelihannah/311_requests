# Washington, DC 311 Requests <img src=https://github.com/hannahelihannah/311_requests/blob/7bb993590be1c54fb06e489e1bb4dac1a51f472f/Flag-District-of-Columbia.jpg width="100" height="60" align="right">

The city of Washington, DC provides 311 as a phone number and request system for city services. This project aims to address the following questions:
> - What variables are most relevant when predicting 311 needs across time and ward?
> - For 311 request purposes, can requestor segmentation add value? i.e. are certain blocks known for having tree-related requests? 
> - What other patterns do we see in 311 requests, and what can we infer from these patterns about city service responsiveness?

Navigate to a specific section using the links below.<br>
[Introduction](#introduction)<br>
[Data Cleansing and Analysis](#data-cleansing-and-analysis)
<br><br>


# Introduction
From the [DC 311 website](https://ouc.dc.gov/page/311-city-services): 
> Examples of typical 311 calls include:

> - Broken meters
> - Trash collection problems or to schedule a bulk pick-up
> - Potholes
> - Abandoned autos
> - Parking enforcement
> - Tree services
> - Illegal dumping
> - Street light repair
> - District agency phone numbers, addresses and hours of operations

Along with the 311 call center, DC also offers an [online 311 portal](https://311.dc.gov/citizen/home) for citizens to submit and track their 311 requests, and a Twitter, [@311DCgov](https://twitter.com/311DCgov), where residents can upload photos of their 311 requests directly.

311 request types vary widely, as do the city agencies that respond to them. Between 2016 and 2020, there were over 1,600,000 311 requests across DC's 8 wards. 


/// EDA across wards, request type by ward, demographics per ward, average response time etc. 
<br>
[Back to top &#8593;](#washington-dc-311-requests-)


# Data Cleansing and Analysis


## Building the Dataset <br />
The first step to analyzing 311 requests across wards was joining the data with American Community Survey data on demographics, socioeconomic characteristics, and housing information across the city's wards. Because this data is based on Census tracts, the Census tract for each address with a 311 request in the system first had to be retrieved via the Census API. NOTE: Though updated 2020 Census tracts were released on August 12, 2021, this project uses 2010 tracts. This may be updated in a future release.

#### ACS Data <br />
The American Community Survey (ACS) is the nation's largest survey of demographic and housing data. When used in tandem with Census information, it can be used to understand demographic changes over time. The survey is conducted by the Census Bureau, though is conducted separately from the actual Census. <br /> The ACS is one of many surveys run by the Census Bureau each year. It differs from the decennial Census in that it's conducted on a sample of households each month of the year to provide up-to-date data to state and local leaders and asks questions that would not appear on the Census, such as internet access and transportation. ACS questions from 2021 and before can be found on their site [here](https://www.census.gov/programs-surveys/acs/methodology/questionnaire-archive.html). <br /> ACS data is available via API from the Census.gov site, but for this project, it was downloaded directly from the [Washington DC Open Data portal](https://opendata.dc.gov/). <br /> The following ACS files were downloaded on July 2, 2021 and used in this project:
> - ACS_Demographic_Characteristics_DC_Ward
> - ACS_Social_Characteristics_DC_Ward
> - ACS_Economic_Characteristics_DC_Census_Tract
> - ACS_Housing_Characteristics_DC_Census_Tract

DC's open data portal also provides visualizations of this data as a standalone dataset - see an example below.<br />
![A map of ACS Housing Characteristics for Washington DC](https://github.com/hannahelihannah/311_requests/blob/efdc69d404b1ac9c206409e5d2e36b8d6868a50b/ACS%20DC%20Housing%20Tract.PNG "ACS Housing DC")
<br />
It's worth noting that there are criticisms of the use of Census and ACS data in the social sciences. Researchers identify three key issues with the data:
> - Undercounting non-immigrant or other at-risk populations
> - Declining response rates over time lead to high variability for salary ranges and other variables
> - Using tracts as proxies for neighborhoods decreases our understanding of how cities function & how residents get access to services.

For the purposes of this project, the first and second criticisms are of greatest interest. For more detail on the third challenge, see Brown University's John Logan's overview for the American Sociological Association [here](https://www.asanet.org/sites/default/files/attach/journals/sept18ccfeaturecombined.pdf). 

/// More on how these challenges were addressed in this project. 
<br>
[Back to top &#8593;](#washington-dc-311-requests-)
<br>

#### 311 Data <br />

In Washington DC, the 311 program helps residents make requests for assistance via city services. Because 311 is always open, DC residents can make requests to the 311 program, which is handled by the Office of Unified Communications, while they're on the go. 311 data is released publicly through Washington DC's Open Data portal, and is grouped into files based on when the requests were made. Users can download files of 311 requests in the last 30 days (35K requests as of this writing) and by year. Starting in 2016, the data changed format, so analysis was completed using data from 2016-2020 - over 1,600,000 311 requests. Key fields in the data are as follows:
> - SERVICECODE: Unique alphanumeric code for service requested (STR)
> - SERVICECODEDESCRIPTION: Longer description of service requested (STR)
> - SERVICETYPECODEDESCRIPTION: Type grouping of service requested (STR)
> - ORGANIZATIONACRONYM: City office assigned to the service request (STR)
> - ADDDATE: Date and time of service request (DATETIME)
> - RESOLUTIONDATE: Date and time of request closure (DATETIME)
> - LATITUDE & LONGITUDE: Two fields representing the latitude and longitude of the request (FLOAT)
> - WARD: Identification of the Ward # of the service request (INT, 1-8)

Though other data fields such as ZIPCODE and XCOORD/YCOORD are present in the data, they are not used - LATITUDE and LONGITUDE provide a more reliable data point to link Census data.

# Predicting 311 Needs by Tract and Time
# Creating Non-Ward, Non-Tract Clusters
# Additional Patterns and Observations




