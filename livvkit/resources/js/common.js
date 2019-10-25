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
    // Used to draw the correct element type
    elementMap = {
        "Error"          : drawError,
        "Summary"        : drawSummary,
        "ValSummary"     : drawValSummary,
        "bookSummary"    : drawValSummary,
        "Diff"           : drawDiff,
        "Bit for Bit"    : drawBitForBit,
        "Gallery"        : drawGallery,
        "Table"          : drawTable,
        "HTML"           : drawHTML
    };

    // Append the generated content
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
    getUrl = window.location.href.substr(0,window.location.href.lastIndexOf('/')+1);
    data = loadJSON(getUrl + indexPath + '/index.json');
    
    // Go through each category: numerics, verification, performance, and validation
    for (var cat in data["Data"]["Elements"]) {
        if (data["Data"]["Elements"][cat] != null && Object.keys(data["Data"]["Elements"][cat]["Data"]).length > 0) {
            if (data["Data"]["Elements"][cat]["Title"] === "Validation" && 
                data["Data"]["Elements"][cat]["Type"] === "ValSummary") {
                html += "<h3>" + data["Data"]["Elements"][cat]["TableTitle"] + "</h3>\n";
            } else if (data["Data"]["Elements"][cat]["Type"] !== "bookSummary") { 
                html += "<h3>" + data["Data"]["Elements"][cat]["Title"] + "</h3>\n";
            }
            // Add the tests for each category
            if (data["Data"]["Elements"][cat]["Type"] === "bookSummary") {
                pageList = Object.keys(data["Data"]["Elements"][cat]["Data"]).sort();
                for (idx in pageList) {
                html += "<h3>" + pageList[idx] + "</h3>\n";
                    for (jdx in data["Data"]["Elements"][cat]["Data"][pageList[idx]]) {
                        html += "<a href=" + indexPath + "/" + data["Data"]["Elements"][cat]["Title"].toLowerCase() + 
                                "/" + jdx + ".html>" + jdx + "</a></br>";
                    }
                }
            } else {
                testList = Object.keys(data["Data"]["Elements"][cat]["Data"]).sort();
                for (idx in testList) {
                    html += "<a href=" + indexPath + "/" + data["Data"]["Elements"][cat]["Title"].toLowerCase() + 
                            "/" + testList[idx] + ".html>" + testList[idx] + "</a></br>";
                }
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
    if (html_file == "") {
        html_file = "index";
    }
    var data = loadJSON('./' + html_file + ".json");
    var html = "<div id=" + data["Title"] + ">";
    if (data["Title"] != "Summary") {
        html += "<h2>" + data["Title"] + "</h2>";
    }
    html += "<p>" + data["Description"];
    html += "</div>";
    $("#content").append(html);
  
    // If there are plain data elements in the dataset draw and add them to the div
    var content = data["Data"];
    if ("Elements" in content) {
        // Add the content
        for (var idx in content["Elements"]) {
            elem = content["Elements"][idx];
            elementMap[elem["Type"]](elem, "#"+data["Title"]);
        }
    }
   
    // If there are tabbed data elements in the dataset draw and add them to the div
    if ("Tabs" in content) {
        // Add the tabs
        var tabs = content["Tabs"];
        tabs = tabs.sort();
        console.log(tabs);

        var html = "<div id=\"tabs\">\n";
        html += "<ul>\n";
        for (var idx in tabs) {
            console.log(idx);
            var tab = tabs[idx];
            html += "<li><a href=\"#" + tab["Title"] + "\">" + 
                    tab["Title"] + "</a></li>\n";
        }
        html += "</ul>\n";

        for (var idx in tabs) {
            console.log(idx);
            var tab = tabs[idx];
            html += "<div id=\"" + tabs[idx]["Title"] + "\"></div>";
        }
        html += "</div>";
        $("#content").append(html);

        // Add the content
        for (var idx in tabs) {
            var tab = tabs[idx];
            if ("Elements" in tab) {
                var elements = tab["Elements"];
                for (var elem_idx in elements) {
                   elem = elements[elem_idx];
                   elementMap[elem["Type"]](elem, "#"+tab["Title"]);
                }
            }
            if ("Sections" in tab) {
                var sections = tab["Sections"];
                for (var tab_idx in sections) {
                    var section  = sections[tab_idx];
                    var section_html =  section['Data'];
                    $("#"+tab["Title"]).append(section_html);
                }
            }
        }
        $("#tabs").tabs();
    }
}


/**
 * Build a summary and adds it to the div.
 *
 * @param {Object} data - The data representing the summary.  Determined by data["Type"] = "Summary"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawSummary(data, div) {
    var html = "<h3>" + data["Title"] + "</h3>";
    html += "<table class=\"summary\">\n";
    // Add the headers
    html += "<th></th>\n";
    for (var header in data["Headers"]) {
        html += "<th>" + data["Headers"][header] + "</th>\n";
    }
    // Add the data
    var testNames = Object.keys(data["Data"]).sort();
    for (var idx in testNames) {
        testName = testNames[idx];
        html += "<tr class=\"testName\"><td>" + testName + "</td></tr>\n";
        for (var testCase in data["Data"][testName]) {
            html_tmp1 = "<tr>";
            html_tmp2 = "\n<td class=\"testCase\">" + testCase + "</td>\n";

            for (var headerIdx in data["Headers"]) {
                header = data["Headers"][headerIdx];
                html_tmp2 += "<td";
                // reset style for each td
                style = "";
                value = data["Data"][testName][testCase][header];
                dtype = typeof value;
                if (dtype == 'number' || dtype == 'string') {
                    html_tmp2 += ">" + value;
                } else if (dtype == 'object') {
                    if (value.length == 2) {
                        // Handle failures
                        if (value[0] != value[1]) {
                            style = " style=\"color:red\"";
                        }
                        html_tmp2 += style + ">";
                        html_tmp2 += value[0] + " of " + value[1];
                    }
                }
                html_tmp2 += "</td>\n";
            }
            html += html_tmp1 + style + html_tmp2 + "</tr>\n";
        }
    }
    html += "</table>\n";
    $(div).append(html);
}

/**
 * Build a validation extension summary and adds it to the div.
 *
 * @param {Object} data - The data representing the summary.  Determined by data["Type"] = "Summary"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawValSummary(data, div) {
    var html = "<h3>" + data["TableTitle"] + "</h3>";
    html += "<table class=\"summary\">\n";
    // Add the headers
    html += "<th></th>\n";
    for (var header in data["Headers"]) {
        html += "<th>" + data["Headers"][header] + "</th>\n";
    }
    // Add the data
    var testNames = Object.keys(data["Data"]).sort();
    for (var idx in testNames) {
        testName = testNames[idx];
        html += "<tr class=\"testName\"><td>" + testName + "</td></tr>\n";
        for (var testCase in data["Data"][testName]) {
            html_tmp1 = "<tr ";
            html_tmp2 = ">\n<td class=\"testCase\">" + testCase + "</td>\n";
            style = "";  
            for (var headerIdx in data["Headers"]) {
                header = data["Headers"][headerIdx];
                html_tmp2 += "<td>"; 
                value = data["Data"][testName][testCase][header];
                dtype = typeof value;
                if (dtype == 'number' || dtype == 'string') {
                    html_tmp2 += value;
                } else if (dtype == 'object') {
                    if (value.length == 2) {
                        html_tmp2 += value[0] + " of " + value[1];
                        // Handle failures
                        if (value[0] != value[1]) {
                            style = "style=\"color:red\"; ";
                        }
                    }
                }
                html_tmp2 += "</td>\n";
            }
            html += html_tmp1 + style + html_tmp2 + "</tr>\n";
        }
    }
    html += "</table>\n";
    $(div).append(html);
}

/**
 * Build an error message and appends it to the div.
 *
 * @param {Object} data - The error element data.  Determined by having data["Type"] = "Error"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawError(data, div) {
    var html = "<div class=\"error\">";
    html += "<h3>" + data["title"] + "</h3>\n";
    html += "<p>ERROR: " + data["message"] + "</p>\n";
    html += "</div>";
    $(div).append(html);
}

/**
 * Build a file diff
 *
 * @param {Object} data - The data representing the table.  Determined by data["Type"] = "Diff"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawDiff(data, div) {
    var html =  data['Data'];
    $(div).append(html);
}

/**
 * Build a bit for bit table
 * 
 * @param {Object} data - The data representing the table.  Determined by 
 *                        data["Type"] = "Bit for Bit"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawBitForBit(data, div) {
    var html = data['Data'];
    $(div).append(html);
}

/**
 * Build a table
 *
 * @param {Object} data - The data representing the table.  Determined by data["Type"] = "Table"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawTable(data, div) {
    var html = data['Data'];
    $(div).append(html);
}

/**
 * Build a gallery
 *
 * @param {Object} data - The data representing the table.  Determined by data["Type"] = "Gallery"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawGallery(data, div) {
    var html = data['Data'];
    $(div).append(html);
}

/**
 * Draw HTML element
 *
 * @param {Object} data - The data representing the html element. Determined by data["Type"] = "HTML"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawHTML (data, div) {
    var html = "<div>";
    html += data["html"];
    html += "</div>";
    $(div).append(html);
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

