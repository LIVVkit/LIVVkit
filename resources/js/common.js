/**
 * When the page is loaded, do some stuff
 */
window.onload = function() {
    var vv_type = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).replace(".html", "");
    console.log(vv_type);
    document.getElementById("content") = drawContent(vv_type);
}

/**
 * Decide what type of content to draw
 */
function drawContent(vv_type) {
    var content = "";
    var sum = "";
    switch(vv_type) {
        case "index":
            content = drawIndex(sum);
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
function drawIndex(indSummary) {
    html = "";

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
