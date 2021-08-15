### Washington, DC - 311 Request History and Predictions
The city of Washington, DC provides 311 as a phone number and request system for city services. 

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

#### Data Cleansing and Analysis
##### Building the Dataset
The first step to analyzing 311 requests across wards was joining the data with American Community Survey data on demographics, socioeconomic characteristics, and housing information across the city's wards. Because this data is based on Census tracts, the Census tract for each address with a 311 request in the system first had to be retrieved via the Census API. 

1. ACS Data <br />
The American Community Survey (ACS) is the nation's largest survey of demographic and housing data. When used in tandem with Census information, it can be used to understand demographic changes over time. The survey is conducted by the Census Bureau, though is conducted separately from the actual Census. <br /> The ACS is one of many surveys run by the Census Bureau each year. It differs from the decennial Census in that it's conducted on a sample of households each month of the year to provide up-to-date data to state and local leaders and asks questions that would not appear on the Census, such as internet access and transportation. ACS questions from 2021 and before can be found on their site [here](https://www.census.gov/programs-surveys/acs/methodology/questionnaire-archive.html). <br /> ACS data is available via API from the Census.gov site, but for this project, it was downloaded directly from the [Washington DC Open Data portal](https://opendata.dc.gov/). <br /> The following ACS files were downloaded on July 2, 2021 and used in this project:
> - ACS_Demographic_Characteristics_DC_Ward
> - ACS_Social_Characteristics_DC_Ward
> - ACS_Economic_Characteristics_DC_Census_Tract
> - ACS_Housing_Characteristics_DC_Census_Tract

DC's open data portal also provides visualizations of this data as a standalone dataset - see an example below.


