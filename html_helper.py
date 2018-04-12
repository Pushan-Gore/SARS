import urllib
import datetime
from datetime import timedelta

class HTMLHelper:
    #start __init__
    def __init__(self):
        self.html = ''
        self.currDate = datetime.datetime.now()
        self.weekDates = []
        #self.weekDates.append(self.currDate.strftime("%Y-%m-%d"))
        self.weekDates.append(self.currDate.strftime("%b %d"))
        for i in range(1,7):
            dateDiff = timedelta(days=-i)
            newDate = self.currDate + dateDiff
            #self.weekDates.append(newDate.strftime("%Y-%m-%d"))
            self.weekDates.append(newDate.strftime("%b %d"))
    #end

    #start getDefaultHTML
    def getDefaultHTML(self, error = 0):
        html = '''
<html>
<head><title>SARS</title>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.4.1/build/cssgrids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="static/styles.css" />
</head>
<body>
    <div class="yui3-g" id="doc">
    <div class="yui3-u" id="hd">
        <h2> Sentiment Analysis </h2>
    </div>
    <div class="yui3-u" id="bd">
        <form name="keyform" id="key-form" method="get" onSubmit="return checkEmpty(this);">
        <p><input type="text" value="" name="keyword" id="keyword"/><input type="submit" value="Submit" id="sub"/></p>
        </form>
'''
        if(error == 1):
            html += '<div id="error">Unable to fetch TWitter API data. Please try again later.</div>'
        elif(error == 2):
            html += '<div id="error">Unrecognized Method of Classfication, please choose one from above.</div>'
        html += '''
    </div>
    <script type="text/javascript">
    function checkEmpty(f) {
        if (f.keyword.value === "") {
            alert('Please enter a valid keyword');
            return false;
        }else{
            f.submit();
            return true;
        }
    }
    var _gaq = _gaq || [];
    _gaq.push(['_setAccount', 'UA-31119754-1']);
    _gaq.push(['_trackPageview']);

    (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
    })();
    </script>
</body>
</html>
'''
        return html
    #end

    #start getResultHTML
    def getResultHTML(self, keyword, results, pos_count, neg_count, neut_count):
        print("Fetched Result web page")
        keyword = urllib.unquote(keyword.replace("+", " "))
        html = '''
<html>
<head><title>SARS</title>
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/3.4.1/build/cssgrids/grids-min.css" />
    <link rel="stylesheet" type="text/css" href="static/styles.css" />
</head>
<body>
    <div class="yui3-g" id="doc">
    <div class="yui3-u" id="hd">
        <h2> Sentiment Analysis </h2>
    </div>
    <div class="yui3-u" id="bd">
        <form name="keyform" id="key-form" method="get" onSubmit="return checkEmpty(this);">
        <p><input type="text" value="" name="keyword" id="keyword"/><input type="submit" value="Search" id="sub"/></p>
        </form>
        <div id="results">
'''
        html += '''
        <div id="result-chart" style="width: 600px; height: 450px;"></div>
        </div>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript">
            google.load("visualization", "1", {packages:["corechart"]});
            google.setOnLoadCallback(drawChart);
            function drawChart() {
                var data = google.visualization.arrayToDataTable([
        '''
        html += "['Sentiment', 'Count'],"
        html += "['Positive',  " + str(pos_count) + "],"
        html += "['Neutral',  " + str(neut_count) + "],"
        html += "['Negative',  " + str(neg_count) + "]"
        html += '''
                ]);

                var options = {
                  'title': 'Sentiment Classification',
                  'pieHole' : 0.4
                };

                var chart = new google.visualization.PieChart(document.getElementById('result-chart'));
                chart.draw(data, options);
            }
            '''

        html += '''
        function checkEmpty(f) {
            if (f.keyword.value === "") {
                alert('Please enter a valid keyword');
                return false;
            }else{
                f.submit();
                return true;
            }
        }
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', 'UA-31119754-1']);
        _gaq.push(['_trackPageview']);

        (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();
    </script>
</body>
</html>
'''
        return html
