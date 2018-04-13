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
<style>
pre {
    background: white;
    font-family: monospace;
    white-space: pre;
    margin: 1em 0;
    padding: 20px;
}
</style>
</head>
<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
        <a class="navbar-brand">Sentiment Analysis</a>
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
    <div class="media">
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
    <br><hr><br>
    <div class="media-body">
        <u><h2 class="media-heading">Naive Bayes Classifiers</h2></u>
<pre>
A classifier based on the Naive Bayes algorithm. In order to find the <br>
probability for a label, this algorithm first uses the Bayes rule to <br>
express P(label|features) in terms of P(label) and P(features|label): <br>
<br>
                       P(label) * P(features|label)                <br>
  P(label|features) = ------------------------------               <br>
                              P(features)                          <br>
<br>
The algorithm then makes the 'naive' assumption that all features are<br>
independent, given the label:<br>
<br>
                       P(label) * P(f1|label) * ... * P(fn|label)<br>
  P(label|features) = --------------------------------------------<br>
                                         P(features)<br>
<br>
Rather than computing P(features) explicitly, the algorithm just<br>
calculates the numerator for each label, and normalizes them so they<br>
sum to one:<br>
<br>
                       P(label) * P(f1|label) * ... * P(fn|label)<br>
  P(label|features) = --------------------------------------------<br>
                        SUM[l]( P(l) * P(f1|l) * ... * P(fn|l) )<br>
</pre>

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
    def getResultHTML(self, keyword, results, pos_count, neg_count, neut_count, tweets, frequency_list):
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
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/d3/3.4.11/d3.min.js"></script>
    <script src="static/cloud.js"></script>
<style>
    .legend {
        border: 1px solid #555555;
        border-radius: 5px 5px 5px 5px;
        font-size: 0.8em;
        margin: 10px;
        padding: 8px;
    }
    .bld {
        font-weight: bold;
    }
</style>
</head>
<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header">
        <a class="navbar-brand">Sentiment Analysis</a>
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
'''

        html += '''
        <div class="media" id="chart"></div>
        <script>
        var frequency_list =
        '''

        html += str(frequency_list)
        html += ''';'''

        html += '''
      drawWordCloud(frequency_list);

      function drawWordCloud(frequency_list){
            var svg_location = "#chart";
            var width = $(document).width();
            var height = $(document).height();

            var fill = d3.scale.category20();

            var word_entries = d3.entries(frequency_list);

            var xScale = d3.scale.linear()
                .domain([0, d3.max(word_entries, function(d) {
                return d.value;
                })
                ])
                .range([10,100]);

            d3.layout.cloud().size([width, height])
                .timeInterval(20)
                .words(word_entries)
                .fontSize(function(d) { return xScale(+d.value); })
                .text(function(d) { return d.key; })
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .on("end", draw)
                .start();

            function draw(words) {
                d3.select(svg_location).append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + [width >> 1, height >> 1] + ")")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return xScale(d.value) + "px"; })
                .style("font-family", "Impact")
                .style("fill", function(d, i) { return fill(i); })
                .attr("text-anchor", "middle")
                .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.key; });
            }

            d3.layout.cloud().stop();
        }
        </script>
        '''

        html += '''
<div class="media" id="result-chart" style="width: 600px; height: 450px; float:right; margin:0 20px 20px 0;"></div>

<div class="container">
<hr>
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
        '''
        html += '''
    </script>
</body>
</html>
'''
        return html
