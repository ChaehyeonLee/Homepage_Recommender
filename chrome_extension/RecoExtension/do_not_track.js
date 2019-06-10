const dont_track_request = new XMLHttpRequest();
const url = "http://54.180.142.66:5000/";

chrome.tabs.getSelected(null, function(tab) {
    document.getElementById('not_url').innerHTML = tab.url;

    dont_track_request.open("POST", url);
    dont_track_request.setRequestHeader("dontTrackRequest", "dont_track_request");
    dont_track_request.send(tab.url);


    dont_track_request.onreadystatechange=function() {
            var track_or_not = dont_track_request.responseText;
            document.getElementById('track_or_not').innerHTML = track_or_not;
    }
    
});


