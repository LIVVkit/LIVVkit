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
        "Vertical Table" : drawVTable,
        "V-H Table"      : drawVHTable,
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
    var verType = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).split("#")[0].replace(".html", "");
    var data = loadJSON('./' + verType + ".json");
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
                    // Draw header
                    var html = "<h2>" + section["Title"] + "</h3>";
                    $("#"+tab["Title"]).append(html);
                    if ("Elements" in section) {
                        var elements = section["Elements"];
                        for (var elem_idx in elements) {
                            elem = elements[elem_idx];
                            elementMap[elem["Type"]](elem, "#"+tab["Title"]);
                        }
                    }          
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
    html += "<h3>" + data["Title"] + "</h3>\n";
    html += "<p>ERROR: " + data["Message"] + "</p>\n";
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
    controller = div.replace("#","") + "_controller";
    // TODO: What's up with this button!?
    var html = "<h3>" + data["Title"] +"</h3>";//+"  <button id=\"" + controller + "\">Hide/Show</button></h3>";
    html += "<div class=\"diff\" id=\""+div+"\">";
    for (var section in data["Data"]) {
        html += "<b>[" + section + "]</b>";
        for (var varName in data["Data"][section]) {
            arr = data["Data"][section][varName];
            // First element determines if the elements matched, otherwise draw what the change was
            if (arr[0]) {
                html += "<p>   " + varName + " = " + arr[1] + "</p>";
            } else {
                html += "<p class=\"new\"> + " + varName + " = " + arr[1] + "</p>";
                html += "<p class=\"old\"> - " + varName + " = " + arr[2] + "</p>";
            }
        }
    }
    html += "</div>";
    $(div).append(html);
    $("."+controller).click(function() {
        $(div).toggle();
    });
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
    var html = "<h3>" + data["Title"] + "</h3>\n";
    html += "<div class=\"bitForBit\">";
    html += "<table>\n";
    html += "<th>Variable</th>\n";
    // Draw the headers
    for (var idx in data["Headers"]) {
        html += "<th>" + data["Headers"][idx] + "</th>\n";
    }
    // Draw the cells
    for (var varName in data["Data"]) {
        html += "<tr>\n";
        html += "<td>" + varName + "</td>\n";
        for (var j in data["Headers"]) {
            var header = data["Headers"][j];
            var hData = data["Data"][varName][header];
            // Handle the different data types to draw (image vs string/numeric data)
            if (header == "Plot" && (hData !== "N/A" || hData.indexOf("ERROR:")!==-1)) {
                var img_dict = {};
                img_dict["Plot File"] = data["Data"][varName][header];
                img_dict["Title"] = varName + "Bit-for-bit compairson";
                html += "<td>" + drawThumbnail(img_dict, 50) + "</td>\n";
            } else {
                if (typeof hData == 'number') {
                    hData = hData.toExponential(5);
                }
                html += "<td>" + hData + "</td>\n";
            }
        }
        html += "</tr>\n";
    }
    html += "</table>\n";
    html += "</div>";
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
    var html = "<h3>" + data["Title"] + "</h3>\n";
    html += "<div class=\"table\">";
    html += "<table>\n";
    // Draw the headers
    for (var idx in data["Headers"]) {
        html += "<th>" + data["Headers"][idx] + "</th>\n";
    }

    // Draw the cells
    html += "<tr>\n";
    for (var idx in data["Headers"]) {
        html += "<td>" + data["Data"][data["Headers"][idx]] + "</td>\n";
    }
    html += "</tr>\n </table>\n </div>";
    $(div).append(html);
}

/**
 * Build a vertical table
 *
 * @param {Object} data - The data representing the table.  Determined by data["Type"] = "Vertical Table"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawVTable(data, div) {
    var html = "<h3>" + data["Title"] + "</h3>\n";
    html += "<div class=\"table\">";
    html += "<table>\n";
    for (var idx in data["Headers"]) {
        html += "<tr>\n";
        // Draw the headers
        html += "<th>" + data["Headers"][idx] + "</th>\n";
        // Draw the cells
        html += "<td>" + data["Data"][data["Headers"][idx]] + "</td>\n";
        html += "</tr>\n";
    }
    html += "</table>\n </div>";
    $(div).append(html);
}

/**
 * Build a table with horizontal and vertical headers and add it to the div.
 *
 * @param {Object} data - The data representing the summary.  Determined by data["Type"] = "V-H Table"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawVHTable(data, div) {
    var html = "<h3>" + data["TableTitle"] + "</h3>";
    html += "<table class=\"table\">\n";
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
            html_tmp2 = ">\n<td>" + testCase + "</td>\n";
            style = "";  
            for (var headerIdx in data["Headers"]) {
                header = data["Headers"][headerIdx];
                html_tmp2 += "<td>"; 
                value = data["Data"][testName][testCase][header];
                dtype = typeof value;
                if (dtype == 'string') {
                    html_tmp2 += value;
                } else if (dtype == 'number') {
                    html_tmp2 += value.toFixed(3);
                } else if (dtype == 'object') {
                    html_tmp2 += " (";
                    for (var v in data["Data"][testName][testCase][header]) {
                        v_val = data["Data"][testName][testCase][header][v];
                        vtype = typeof v_val;
                        if (vtype == 'number') {
                            html_tmp2 += v_val.toExponential(3);
                        } else {
                            html_tmp2 += v_val;
                            html_tmp2 += vtype;
                        }
                        html_tmp2 += ", ";
                    }
                    html_tmp2 = html_tmp2.replace(/, $/, '');
                    html_tmp2 += ")";
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
 * Build a gallery
 *
 * @param {Object} data - The data representing the table.  Determined by data["Type"] = "Gallery"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawGallery(data, div) {
    var html = "<div class=\"gallery\">";
    html += "<h3>" + data["Title"] + "</h3>";
    html += "</div>";

    // Create the gallery div to put all the images into
    $(div).append(html);
    
    for (var idx in data["Data"]) {
        img_elem = data["Data"][idx];
        // Draw an image 
        drawImage(img_elem, div+" > div.gallery");
    }
    
    $(div).append("<div style=\"clear:both\"></div>");
}

/**
 * Draw an image
 *
 * @param {Object} data - The data representing the image.  Determined by data["Type"] = "Image"
 * @param {string} div - The name of the div to draw to.  Should be referenced as a string that 
 *                       determines whether it is a class or id (ie include # or .)
 */
function drawImage(img_elem, div) {
    var html = "<div>";
    html += drawLightbox(img_elem);
    html += "</div>"
    $(div).append(html);
}

/**
 * Draw an image thumbnail with a link to open the image in a lightbox 
 *
 * @param {dictionary} img_elem  - Dictionary describing the image location, title, album, and caption
 * @param {number} size - The desired height to draw
 *
 * @return the html to embed into another element
 */
function drawLightbox(img_elem) {
    var img_dir = window.location.href.substr(0,window.location.href.lastIndexOf('/')+1) + "imgs/";
    var path = img_dir + img_elem["Plot File"];
    var lbox = img_elem["Group"] ? img_elem["Group"]  : img_elem["Title"];
    var size = img_elem["Height"] ? img_elem["Height"]  : 200;
    var html = "<a href=\"" + path + "\" data-lightbox=\"" + lbox + "\" data-title=\"" + img_elem["Description"] + "\">";
    html += "<img class=\"thumbnail caption\" data-caption=\"" + img_elem["Title"]+ "\" alt=\"" + img_elem["Title"] + "\" src=\"" + path + "\" style=\"height: " + size + "px; overflow: hidden; position: relative\">";
    html += "</a>";
    return html;
}

/**
 * Draw an image thumbnail with a link to open in a new tab 
 *
 * @param {string} path - The location of the image to thumbnail-size 
 * @param {number} size - The desired height to draw
 *
 * @return the html to embed into another element
 */
function drawThumbnail(img_elem, size) {
    var img_dir = window.location.href.substr(0,window.location.href.lastIndexOf('/')+1) + "imgs/";
    var path = img_elem["Plot File"];
    var html = "<a target=\"_blank\" href=\"" + path + "\">";
    html += "<img class=\"thumbnail\" alt=\"" + img_elem["Title"] + "\" src=\"" + path + "\" style=\"height: " + size + "px; overflow: hidden; position: relative\">";
    html += "</a>";
    return html;
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
    html += data["Data"];
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

