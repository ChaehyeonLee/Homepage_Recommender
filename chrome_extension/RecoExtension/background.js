chrome.browserAction.onClicked.addListener(function(tab) {
    chrome.tabs.executeScript(null, {file: "do_not_track.js"});
 });

// function hasOneDayPassed() {
//   // get today's date. eg: "7/37/2007"
//   var date = new Date().toLocaleDateString();

//   // if there's a date in localstorage and it's equal to the above: 
//   // inferring a day has yet to pass since both dates are equal.
//   if( localStorage.yourapp_date == date ) 
//       return false;

//   // this portion of logic occurs when a day has passed
//   localStorage.yourapp_date = date;
//   return true;
// }

// // some function which should run once a day
// function runOncePerDay(){
//     if( !hasOneDayPassed() ) return false;

//     // your code below
//     alert('Good morning!');
//     http_send_history.open("POST", url);
//     http_send_history.setRequestHeader("sendHistory", "send_history");
//     chrome.history.search({
//         'text': '',
//         'startTime': sixMonthAgo,
//         'maxResults': 15000,
//         }, function(historyItems){
//             for (var i = 0; i < historyItems.length; ++i) {
//                 var url = historyItems[i].url;
//                 var visitCount = historyItems[i].visitCount;
//                 var processVisitsWithUrl = function(url, visitCount) {
//                     return function(visitItems) {
//                         processVisits(url, visitItems, visitCount);
//                     };
//                 };
                
//                 chrome.history.getVisits({url: url}, processVisitsWithUrl(url, visitCount));
//                 numRequestsOutstanding++;
//             };
//             if (!--numRequestsOutstanding) {
//                 onAllVisitsProcessed();
//             }
//         }
//     );
//     http_send_history.onreadystatechange=function() {
//     if(this.readyState===4 && this.status===200) {
//         alert(http_send_history.responseText);
//     }
// }
//   }
  
  
// runOncePerDay(); // run the code
// runOncePerDay(); // does not run the code

// const url = 'http://54.180.142.66:5000/';
// const http_send_history = new XMLHttpRequest();
// var visit_history = new Array();
// var numRequestsOutstanding = 0;
// var microsecondsPerWeek = 1000 * 60 * 60 * 24 * 7;
// var microsecondsPerSixMonth = microsecondsPerWeek * 4 * 6;
// var sixMonthAgo = (new Date).getTime() - microsecondsPerSixMonth;


// var processVisits = function(url, visitItems, visitCount) {
//     for (var i = 0, ie = visitItems.length; i < ie; ++i) {
//         var visit_data = new Object();
//         visit_data.url = url;
//         visit_data.visit_time = visitItems[i].visitTime;
//         visit_data.visit_count = visitCount;
//         visit_history.push(visit_data);
//     }
//     if (!--numRequestsOutstanding) {
//         onAllVisitsProcessed();
//       }
//   };

// var onAllVisitsProcessed = function() {
//     http_send_history.send(JSON.stringify(visit_history));
// }
