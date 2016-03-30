/**
 * When the page is loaded, do some stuff
 */
$(document).ready(function() {
    // Figure out what we are going to draw
    var vv_type = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).replace(".html", "");
    
    // Used to draw the correct element type
    elementMap = {
        "Summary" : drawSummary,
        "Table" : drawTable,
        "Gallery" : drawGallery
    }

    // Append the generated content
    $('#content').append(drawContent(vv_type));
});

/**
 * Branch on the type of content
 */
function drawContent(vv_type) {
    var content = "";
    switch(vv_type) {
        case "index":
            content = drawIndex();
            break;
        case "verification":
            content = drawVerification(sum);
            break;
        case "validation":
            content = drawValidation(sum);
            break;
        case "performance":
            content = drawPerformance(sum);
            break;
        case "numerics":
            content = drawNumerics(sum);
            break;
    }
    return content;
}

/**
 * Generatees the summary content page
 */
function drawIndex() {
    html = "";
    var data = loadJSON('./index.json');
    for (var cat in data) {
        if (data[cat] != null) {
            html += "<h1>" + cat + "</h1>\n";
            elemType = data[cat]["meta-data"]["Format"];
            html += elementMap[data[cat]["meta-data"]["Format"]](data[cat]["meta-data"],data[cat]["test-data"]);
        }
    }
    return html;
}


/**
 * Generates the verification content page
 */
function drawVerification(verSummary) {
    html = "";
    return html;
}


/**
 * Generates the validation content page
 */
function drawValidation(valSummary) {
    html = "";
    return html;
}


/**
 * Generates the performance content page
 */
function drawPerformance(perfSummary) {
    html = "";
    return html;
}


/**
 * Generates the numerics content page
 */
function drawNumerics(numSummary) {
    html = "";
    return html;
}


/**
 * Build a summary 
 */
function drawSummary(meta, data) {
    var tableHTML = "<table>\n";
  
    // Add the headers
    tableHTML += "<th></th>\n";
    for (var header in meta["Headers"]) {
        tableHTML += "<th>" + meta["Headers"][header] + "</th>\n";
    }
            
    // Add the data
    for (var testName in data) {
        tableHTML += "<tr class=\"testName\"><td>" + testName + "</td></tr>\n";
        for (var testCase in data[testName]) {
            html_tmp1 = "<tr ";
            html_tmp2 = ">\n<td class=\"testCase\">" + testCase + "</td>\n";
            for (var headerIdx in meta["Headers"]) {
                header = meta["Headers"][headerIdx];
                html_tmp2 += "<td>"; 
                value = data[testName][testCase][header];
                dtype = typeof value;
                style = "";  
                if (dtype == 'number') {
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
            tableHTML += html_tmp1 + style + html_tmp2 + "</tr>\n";
        }
    }
    
    tableHTML += "</table>\n";
    return tableHTML;
}


/**
 * Build a table
 */
function drawTable(meta, data) {
    var tableHTML = "";
    return tableHTML;
}


/**
 * Build a gallery
 */
function drawGallery(meta, data) {
    var galleryHTML = "";
    return galleryHTML;
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

