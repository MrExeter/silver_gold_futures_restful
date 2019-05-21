# Test API for pulling commodities data from a website.

#### This test API pulls recent commodity data for Gold, Silver and other commodities, 

Current list of commodities.

* Gold
* Silver
* Platinum
* Copper
* Brent
* West Texas Intermediate -> 'wti'
* Natural Gas -> 'nat_gas'
* Heating Oil -> 'heating_oil'

<hr>


### To build container
### docker build -t flaskapp:latest .
### docker run -it -d -p 8080:8080 flaskapp
<hr>

#### When container is running, use a call like this to receive formatted price data

#### curl "http://127.0.0.1:8080/commodity?start_date=2017-05-10&end_date=2017-05-22&commodity_type=gold"
#### or use Postman for a get request and supply json data parameters giving the commodity name and a valid date range

{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"commodity_type": "silver",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"start_date": "2017-05-10",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"end_date": "2017-05-22"  
}  

