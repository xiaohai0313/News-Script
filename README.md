# News-Script

Back-end server

- Use the cloud backend code in Flask/Python for all calls to Google News
- The cloud backend code receives JSON from Google News and returns it to the client, possibly filtered and modified (see below)
- The cloud back end is a "proxy" to Google News

Front-end client

- Use XMLHttpRequest/json.Parse() in asynchronous mode to call the Flask/JSON back-end REST-ful API entry points
- No calls using XMLHttpRequest should be done to Google News APIs
- JavaScript / DOM handle all front-end "dynamic" manipulation
- Use D3 library functions for "word cloud"

Flask/Python

- Flask is used for implement RESTful services to Google News
- Flask templates is not be used for any other functionality that dynamically combines Python with HTML
- Flask use send_static_file to send "static" HTML, CSS and JavaScript
- Count the frequency of words and remove stopwords in the backend and append it to the returning data from Google News, coded in pure Python (to prepare data D3 needs)
- filter null values and return only 5 valid articles for home page 

demo screenshot
![home](https://github.com/xiaohai0313/News-Script/blob/master/page1.png)
![search](https://github.com/xiaohai0313/News-Script/blob/master/page2.png)
