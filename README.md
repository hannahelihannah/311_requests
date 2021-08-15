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

