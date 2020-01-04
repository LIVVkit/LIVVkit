/*
/ Copyright (c) 2015-2018, UT-BATTELLE, LLC
/ All rights reserved.
/ 
/ Redistribution and use in source and binary forms, with or without
/ modification, are permitted provided that the following conditions are met:
/ 
/ 1. Redistributions of source code must retain the above copyright notice, this
/ list of conditions and the following disclaimer.
/ 
/ 2. Redistributions in binary form must reproduce the above copyright notice,
/ this list of conditions and the following disclaimer in the documentation
/ and/or other materials provided with the distribution.
/ 
/ 3. Neither the name of the copyright holder nor the names of its contributors
/ may be used to endorse or promote products derived from this software without
/ specific prior written permission.
/ 
/ THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
/ ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
/ WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
/ DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
/ FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
/ DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
/ SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
/ CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
/ OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
/ OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
/ */


/**
 * When the page is loaded, do some stuff
 */
$(document).ready(function() {
    drawNav();
    drawContent();
});

$(window).load(function() {
    $('img.caption').captionjs();
});


/**
 * Draws the navigation sidebar by looking at the index.json data and appends the 
 * list of resultant pages to the nav div.
 */
function drawNav() {
    // Get the dataset, to do so the html page must have the `indexPath` variable defined
    var html = "";
    var getUrl = window.location.href.substr(0,window.location.href.lastIndexOf('/')+1);
    var data = loadJSON(getUrl + indexPath + '/index.json');
    data = data["Page"];
    // Go through each category: numerics, verification, performance, and validation
    for (var el_idx in data["elements"]) {
        if (data["elements"][el_idx] != null && Object.keys(data["elements"][el_idx]["Table"]["data"]).length > 0) {
            html += "<h3>" + data["elements"][el_idx]["Table"]["title"] + "</h3>\n";
            var testList = Array.from(new Set( data["elements"][el_idx]["Table"]["index"])).sort();
            for (var idx in testList) {
                html += "<a href=" + indexPath + "/" + data["elements"][el_idx]["Table"]["title"].toLowerCase() +
                        "/" + testList[idx] + ".html>" + testList[idx] + "</a></br>";
            }
        }
    }
    $("#nav").append(html);
}


/**
 * Draws content to the page by looking at the name of the page and loading the 
 * appropriate dataset.
 */
function drawContent() {
    // Load the data and add header information
    var html_file = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).split("#")[0].replace(".html", "");
    // Assume index.html if empty page name
    if (html_file === "") {
        html_file = "index";
    }
    var data = loadJSON('./' + html_file + ".json");
    var html = data["Page"]["Data"];
    $("#content").append(html);
    $("#tabs").tabs();
}

/**
 * Load a json file into a variable
 */
function loadJSON(path) {
    var data;
    $.ajax({
        'async': false,
        'global': false,
        'url': path,
        'dataType': "json",
        'success': function(json) {
            data = json;
        }
    });
    return data;
}

