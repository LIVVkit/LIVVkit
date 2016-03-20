/**
 * When the page is loaded, do some stuff
 */
window.onload = function() {
    var vv_type = window.location.href.substr(
            window.location.href.lastIndexOf("/")+1).replace(".html", "");
    console.log(vv_type);
    document.getElementById("content") = drawContent(vv_type);
};

/**
 * Decide what type of content to draw
 */
function drawContent(vv_type) {
    var content = "";
    switch(vv_type) {
        case "index":
            content = drawIndex(summary);
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
function drawIndex(data) {
    html = "<h1>Verification</h1>";
    console.log(data)
    for (var category in data) {
        html += "<table>";
        
        // Get a list of all of the headers
        for (var test in data[category]) {
            headers = [];
            for (var v in data[category][test]) {
                headers.push(v);
            }
        }
        headers = unique(headers);
        
        // Draw the headers
        html += "<tr><th>"+category+"</th>";
        for (var i=0; i<headers.length; i++) {
          html += "<th>" + headers[i] + "</th>";  
        }
        html += "</tr>";
        
        // Fill in the table
        for (var test in data[category]) {    
            html += "<tr> <td>" + test + "</td>";
            for (var i=0; i<headers.length; i++) {
                var inner_td = "class=maybe>No data available.";
                 
                if (data[category][test].hasOwnProperty(headers[i])) {
                    switch(headers[i]) {
                        case "BitForBit":
                            var b4b = data[category][test][headers[i]];
                            if (b4b[0] == b4b[1]){
                                inner_td = "class=good>" + b4b[0] + " of " + b4b[1];
                            } else {
                                inner_td = "class=bad>" + b4b[0] + " of " + b4b[1];
                            }
                            break;
                        case "ConfigMatched":
                            var cfg = data[category][test][headers[i]];
                            if (cfg[0] == cfg[1]) {
                                inner_td = "class=good>" + cfg[0] + " of " + cfg[1];
                            } else {
                                inner_td = "class=bad>" + cfg[0] + " of " + cfg[1];
                            }
                            break;
                        default:
                            inner_td = ">" + data[category][test][headers[i]];
                    }
                }
                html += "<td " + inner_td + "</td>"
            }
            html += "</tr>";
        }
        html += "</tr></table>";
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
