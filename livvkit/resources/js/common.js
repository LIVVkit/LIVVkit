/**
 * When the page is loaded, do some stuff
 */
$(document).ready(function() {
    // Used to draw the correct element type
    elementMap = {
        "Error" : drawError,
        "Summary" : drawSummary,
        "Table" : drawTable,
        "Bit for Bit" : drawBitForBit,
        "Diff" : drawDiff,
        "Gallery" : drawGallery
    };

    // Used to draw the correct page
    contentMap = {
        "index" : drawIndex,
        "verification" : drawVerification,
        "validation" : drawValidation,
        "performance" : drawPerformance,
        "numerics" : drawNumerics
    };

    // Append the generated content
    drawNav();
    contentMap[vvType]();
});


/**
 * Draw the navigation sidebar
 */
function drawNav() {
    html = "";
    getUrl = window.location.href.substr(0,window.location.href.lastIndexOf('/')+1);
    data = loadJSON(getUrl + indexPath + '/index.json');
    console.log(getUrl + indexPath + '/index.json');
    for (var cat in data["Elements"]) {
        if (data["Elements"][cat] != null && Object.keys(data["Elements"][cat]["Data"]).length > 0) {
            html += "<h3>" + data["Elements"][cat]["Title"] + "</h3>\n";
            testList = Object.keys(data["Elements"][cat]["Data"]).sort();
            for (idx in testList) {
                html += "<a href=" + indexPath + "/" + data["Elements"][cat]["Title"].toLowerCase() + "/" + testList[idx] + ".html>" + testList[idx] + "</a></br>";
            }
        }
    }
    $("#nav").append(html);
}


/**
 * Generatees the summary content page
 */
function drawIndex() {
    var data = loadJSON(indexPath + '/index.json');
    for (var cat in data["Elements"]) {
        console.log(data["Elements"][cat]);
        if (data["Elements"][cat] != null && Object.keys(data["Elements"][cat]["Data"]).length > 0) {
            $("#content").append("<h1>" + data["Elements"][cat]["Title"] + "</h1>");
            elemType = data["Elements"][cat]["Type"];
            elementMap[elemType](data["Elements"][cat], "#content");
        }
    }
}


/**
 * Generates the verification content page
 */
function drawVerification() {
    var verType = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).split("#")[0].replace(".html", "");
    var data = loadJSON('./' + verType + ".json");
    var testCases = Object.keys(data).sort();
    
    // Add the tabs
    html = "<div id=\"tabs\">\n";
    html += "<ul>\n";
    for (var idx in testCases) {
        html += "<li><a href=\"#" + testCases[idx] + "\">" + testCases[idx] + "</a></li>\n";
    }
    html += "</ul>\n";
    for (var idx in testCases) {
        html += "<div id=\"" + testCases[idx] + "\"></div>";
    }
    html += "</div>";
    $("#content").append(html);

    // Add the content
    for (var idx in testCases) {
        testName = testCases[idx];
        for (var subcase in data[testCases[idx]]) {
            section = data[testName][subcase];
            sectionName = testName + "_" + subcase;
            $("#"+testName).append("<div id=\"" + sectionName + "\"></div>");
            $("#"+sectionName).append("<h1>" + section["Title"] + "</h1>");
            for (var idx2 in data[testCases[idx]][subcase]["Elements"]) {
                elem = section["Elements"][idx2];
                elementMap[elem["Type"]](elem, "#"+sectionName);
            }
        }
    }
    $("#tabs").tabs();
}


/**
 * Generates the validation content page
 */
function drawValidation() {
    var verType = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).split("#")[0].replace(".html", "");
    var data = loadJSON('./' + verType + ".json");
     
    html = "<div id=" + data["Title"] + ">";
    html += "<h2>" + data["Title"] + "</h2>";
    html += "<p>" + data["Description"];
    html += "</div>";
    $("#content").append(html); 
    
    // Add the content
    for (var idx in data["Elements"]) {
        elem = data["Elements"][idx];
        elementMap[elem["Type"]](elem, "#"+data["Title"]);
    }
}


/**
 * Generates the performance content page
 */
function drawPerformance() {
    var verType = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).split("#")[0].replace(".html", "");
    var data = loadJSON('./' + verType + ".json");
     
    html = "<div id=" + data["Title"] + ">";
    html += "<h2>" + data["Title"] + "</h2>";
    html += "<p>" + data["Description"];
    html += "</div>";
    $("#content").append(html); 
    
    // Add the content
    for (var idx in data["Elements"]) {
        elem = data["Elements"][idx];
        elementMap[elem["Type"]](elem, "#"+data["Title"]);
    }
}


/**
 * Generates the numerics content page
 */
function drawNumerics() {
    var verType = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).split("#")[0].replace(".html", "");
    var data = loadJSON('./' + verType + ".json");
     
    html = "<div id=" + data["Title"] + ">";
    html += "<h2>" + data["Title"] + "</h2>";
    html += "<p>" + data["Description"];
    html += "</div>";
    $("#content").append(html); 
    
    // Add the content
    for (var idx in data["Elements"]) {
        elem = data["Elements"][idx];
        elementMap[elem["Type"]](elem, "#"+data["Title"]);
    }
}


/**
 * Build a table
 */
function drawSummary(data, div) {
    var html = "<table class=\"summary\">\n";
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
                console.log(dtype);
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
 * Build an error message
 */
function drawError(data, div) {
    html = "<h3>" + data["Title"] + "</h3>\n";
    html += "<div class=\"error\">";
    html += "<p>ERROR: " + data["Message"] + "</p>\n";
    html += "</div>";
    $(div).append(html);
}


/**
 * Build a diff
 */
function drawDiff(data, div) {
    controller = div.replace("#","") + "_controller";
    // TODO: What's up with this button!?
    html = "<h3>" + data["Title"] +"</h3>";//+"  <button id=\"" + controller + "\">Hide/Show</button></h3>";
    html += "<div class=\"diff\" id=\""+div+"\">";
    for (var section in data["Data"]) {
        html += "<b>[" + section + "]</b>";
        for (var varName in data["Data"][section]) {
            arr = data["Data"][section][varName];
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
 */
function drawBitForBit(data, div) {
    html = "<h3>" + data["Title"] + "</h3>\n";
    html += "<div class=\"bitForBit\">";
    html += "<table>\n";
    html += "<th>Variable</th>\n";
    for (var idx in data["Headers"]) {
        html += "<th>" + data["Headers"][idx] + "</th>\n";
    }
    for (var varName in data["Data"]) {
        html += "<tr>\n";
        html += "<td>" + varName + "</td>\n";
        for (var j in data["Headers"]) {
            var header = data["Headers"][j];
            var hData = data["Data"][varName][header];
            if (header == "Plot" && (hData !== "N/A" || hData.indexOf("ERROR:")!==-1)) {
                html += "<td>" + drawThumbnail(hData, 50) + "</td>\n";
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
 */
function drawTable(data, div) {
    html = "<h3>" + data["Title"] + "</h3>\n";
    html += "<div class=\"table\">";
    html += "<table>\n";
    for (var idx in data["Headers"]) {
        html += "<th>" + data["Headers"][idx] + "</th>\n";
    }

    html += "<tr>\n";
    for (var idx in data["Headers"]) {
        html += "<td>" + data["Data"][data["Headers"][idx]] + "</td>\n";
    }
    html += "</tr>\n";
    html += "</table>\n";
    html += "</div>";
    $(div).append(html);
}


/**
 * Build a gallery
 */
function drawGallery(data, div) {
    var html = "<div class=\"gallery\">";
    html += "<h3>" + data["Title"] + "</h3>";
    html += "</div>";
    $(div).append(html);
    for (var idx in data["Data"]) {
        img_elem = data["Data"][idx];
        $(".gallery").append("<div id=img_"+idx+"></div>")
        drawImage(img_elem, $("#img_"+idx));
    }
}


function drawImage(img_elem, div) {
    img_dir = window.location.href.substr(0,window.location.href.lastIndexOf('/')+1) + "imgs/";
    var html = "<p>" + img_elem["Title"] + "</p>";
    html += drawThumbnail(img_dir + img_elem["Plot File"], 200);
    $(div).append(html);
}


function drawThumbnail(path, size) {
    html = "<a target=\"_blank\" href=\"" + path + "\">";
    html += "<img src=\"" + path + "\" style=\"height: " + size + "px; overflow: hidden; position: relative\">";
    html += "</a>";
    return html;
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

/**
 * Recursively go through json data and search for the "Elements" list
 */
function getElements(json) {
    if (json.hasOwnProperty("Elements")) {
        return json["Elements"];
    } else { 
        for (section in json) {
            return getElements(json[section]);
        }
    }
}

