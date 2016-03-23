/**
 * When the page is loaded, do some stuff
 */
$(document).ready(function() {
    var vv_type = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).replace(".html", "");
    $('#content').append(drawContent(vv_type));
});

/**
 * Decide what type of content to draw
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
    console.log(data); 
    for (var cat in data) {
        if (data[cat] != null) {
            html += "<h1>" + cat + "</h1>\n";
            html += "<table>\n";
            
            html += "<th></th>\n";
            for (var header in data[cat]["Metadata"]["Headers"]) {
                html += "<th>" + data[cat]["Metadata"]["Headers"][header] + "</th>\n";
            }
            
            var dtype;
            for (var testName in data[cat]) {
                if (testName != "Metadata") {
                    html += "<tr class=\"testName\"><td>" + testName + "</td></tr>\n";
                    for (var testCase in data[cat][testName]) {
                        html += "<tr>\n";
                        html += "<td>" + testCase + "</td>\n";
                        for (var headerIdx in data[cat]["Metadata"]["Headers"]) {
                            header = data[cat]["Metadata"]["Headers"][headerIdx];
                            html += "<td>"; 
                            value = data[cat][testName][testCase][header];
                            dtype = typeof value;
                            
                            if (dtype == 'number') {
                                html += value;
                            } else if (dtype == 'object') {
                                if (value.length == 2) {
                                    html += value[0] + " of " + value[1];
                                }
                            }
                            html += "</td>\n";
                        }
                        html += "</tr>\n";
                    }
                }
            }
            
            html += "</table>\n";
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

