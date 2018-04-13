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
<html lang="en">
<head>
    <title>SARS</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
        <a class="navbar-brand" href="#">Sentiment Analysis</a>
    </div>
    <form class="navbar-form navbar-right" name="keyform" method="get" onSubmit="return checkEmpty(this);">
        <div class="input-group">
            <input type="text" class="form-control" placeholder="Search" name="keyword">
            <div class="input-group-btn">
                <button class="btn btn-default" type="submit">
                    <i class="glyphicon glyphicon-search"></i>
                </button>
            </div>
        </div>
    </form>
  </div>
</nav>

<div class="container">
    </br>
    <h2>About the Project</h2>
    <h3>
        <p> This is a sentiment analyzer </p>
        <p> Performing sentiment analysis on movie reviews, </p>
        <p> the analyzer uses Naive-Bayes classifier technique</p>
    </h3>
    </br></br></br>
    <h2>Usage</h2>
    <h3>
        <p> Enter the movie in the search bar and press enter </p>
    </h3>
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
    def getResultHTML(self, keyword, results, pos_count, neg_count, neut_count, tweets):
        print("Fetched Result web page")
        keyword = urllib.unquote(keyword.replace("+", " "))
        html = '''
<html>
<head><title>SARS</title>
    <title>SARS</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
        <a class="navbar-brand" href="#">Sentiment Analysis</a>
    </div>
    <form class="navbar-form navbar-right" name="keyform" method="get" onSubmit="return checkEmpty(this);">
        <div class="input-group">
            <input type="text" class="form-control" placeholder="Search" name="keyword">
            <div class="input-group-btn">
                <button class="btn btn-default" type="submit">
                    <i class="glyphicon glyphicon-search"></i>
                </button>
            </div>
        </div>
    </form>
  </div>
</nav>

<div class="media" id="result-chart" style="width: 600px; height: 450px; float:right; margin:0 20px 20px 0;"></div>

<div class="container">
    <div class="media">
        <div class="media-body">
            <h4 class="media-heading"></h4>
            <p></p>
        </div>
    </div>
<hr>


'''
        html += '''
        <div class="media-body">
        '''
        #Printing tweets here
        html += '''
            <h4 class="media-heading">Positive Tweets</h4>
            <hr>
        '''
        count = 0
        for tweet in tweets:
            if(tweet['sentiment'] == 'pos'):
                html += '''<p>'''
                html += tweet['text']
                html += '''</p>'''
                count = count + 1
            if(count == 11):
                break

        html += '''
            <br><hr>
            <h4 class="media-heading">Negative Tweets</h4>
            <hr>
        '''

        count = 0
        for tweet in tweets:
            if(tweet['sentiment'] == 'neg'):
                html += '''<p>'''
                html += tweet['text']
                html += '''</p>'''
                count = count + 1
            if(count == 11):
                break

        html += '''
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
