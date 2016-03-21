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
    var data;
    $.ajax({
        'async': false,
        'global': false,
        'url': './index.json',
        'dataType': "json",
        'success': function(json) {
            data = json;
        }
    });
    console.log(data);   
    for (var cat in data) {
        if (data[cat] != null) {
            html += "<h1>" + cat + "</h1>\n";
            html += "<table>\n";

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
