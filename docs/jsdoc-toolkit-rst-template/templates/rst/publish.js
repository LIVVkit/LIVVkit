/** Called automatically by JsDoc Toolkit. */
function publish(symbolSet) {
  publish.conf = {  // trailing slash expected for dirs
    ext:         ".rst",
    outDir:      JSDOC.opt.d || SYS.pwd+"../out/jsdoc/",
    templatesDir: JSDOC.opt.t || SYS.pwd+"../templates/jsdoc/",
    symbolsDir:  "symbols/",
    srcDir:      "symbols/src/"
  };

  // If source output is suppressed, just display the links to the source file
  if (JSDOC.opt.s && defined(Link) && Link.prototype._makeSrcLink) {
    Link.prototype._makeSrcLink = function(srcFilePath) {
      return "<"+srcFilePath+">";
    }
  }
  
  // create the folders and subfolders to hold the output
  IO.mkPath((publish.conf.outDir+"symbols/src").split("/"));
    
  // used to allow Link to check the details of things being linked to
  Link.symbolSet = symbolSet;

  // create the required templates
  try {
    var classTemplate = new JSDOC.JsPlate(publish.conf.templatesDir+"class.tmpl");
    var classesTemplate = new JSDOC.JsPlate(publish.conf.templatesDir+"allclasses.tmpl");
  }
  catch(e) {
    print("Couldn't create the required templates: "+e);
    quit();
  }

  // Some utility filters
  function hasNoParent($) {return ($.memberOf == "")}
  function isaFile($) {return ($.is("FILE"))}
  function isaClass($) {return ($.is("CONSTRUCTOR") || $.isNamespace )}
  //function isaNamespace($) {return ($.isNamespace)}
  
  // get an array version of the symbolset, useful for filtering
  var symbols = symbolSet.toArray();
  
  // create the hi-lighted source code files
  // TODO: restore the src file generation
  var files = JSDOC.opt.srcFiles;
  /*
  for (var i = 0, l = files.length; i < l; i++) {
    var file = files[i];
    var srcDir = publish.conf.outDir + "symbols/src/";
    makeSrcFile(file, srcDir);
  }
  */
  
  // get a list of all the classes in the symbolset
  var classes = symbols.filter(isaClass).sort(makeSortby("alias"));
  // test
  //var classes = symbols.filter(isaNamespace).sort(makeSortby("alias"));
  
  // create a filemap in which outfiles must be to be named uniquely, ignoring case
  if (JSDOC.opt.u) {
    var filemapCounts = {};
    Link.filemap = {};
    for (var i = 0, l = classes.length; i < l; i++) {
      var lcAlias = classes[i].alias.toLowerCase();
      
      if (!filemapCounts[lcAlias]) filemapCounts[lcAlias] = 1;
      else filemapCounts[lcAlias]++;
      
      Link.filemap[classes[i].alias] = 
        (filemapCounts[lcAlias] > 1)?
        lcAlias+"_"+filemapCounts[lcAlias] : lcAlias;
    }
  }
  
  // create a class index, displayed in the left-hand column of every class page
  Link.base = "../";
  publish.classesIndex = classesTemplate.process(classes); // kept in memory
  
  // create each of the class pages
  for (var i = 0, l = classes.length; i < l; i++) {
    var symbol = classes[i];
    
    symbol.events = symbol.getEvents();   // 1 order matters
    symbol.methods = symbol.getMethods(); // 2
    
    var output = "";
    output = classTemplate.process(symbol);
    
    IO.saveFile(publish.conf.outDir+"symbols/", ((JSDOC.opt.u)? Link.filemap[symbol.alias] : symbol.alias) + publish.conf.ext, output);
  }
  
  // regenerate the index with different relative links, used in the index pages
  Link.base = "";
  publish.classesIndex = classesTemplate.process(classes);
  
  // create the class index page
  try {
    var classesindexTemplate = new JSDOC.JsPlate(publish.conf.templatesDir+"index.tmpl");
  }
  catch(e) { print(e.message); quit(); }
  
  var classesIndex = classesindexTemplate.process(classes);
  IO.saveFile(publish.conf.outDir, "index"+publish.conf.ext, classesIndex);
  classesindexTemplate = classesIndex = classes = null;
  
  // create the file index page
  try {
    var fileindexTemplate = new JSDOC.JsPlate(publish.conf.templatesDir+"allfiles.tmpl");
  }
  catch(e) { print(e.message); quit(); }
  
  var documentedFiles = symbols.filter(isaFile); // files that have file-level docs
  var allFiles = []; // not all files have file-level docs, but we need to list every one
  
  for (var i = 0; i < files.length; i++) {
    allFiles.push(new JSDOC.Symbol(files[i], [], "FILE", new JSDOC.DocComment("/** */")));
  }
  
  for (var i = 0; i < documentedFiles.length; i++) {
    var offset = files.indexOf(documentedFiles[i].alias);
    allFiles[offset] = documentedFiles[i];
  }
    
  allFiles = allFiles.sort(makeSortby("name"));

  // output the file index page
  var filesIndex = fileindexTemplate.process(allFiles);
  IO.saveFile(publish.conf.outDir, "files"+publish.conf.ext, filesIndex);
  fileindexTemplate = filesIndex = files = null;
}


/** Just the first sentence (up to a full stop). Should not break on dotted variable names. */
function summarize(desc) {
  if (typeof desc != "undefined")
    return desc.match(/([\w\W]+?\.)[^a-z0-9_$]/i)? RegExp.$1 : desc;
  return desc;
}

/** Make a symbol sorter by some attribute. */
function makeSortby(attribute) {
  return function(a, b) {
    if (a[attribute] != undefined && b[attribute] != undefined) {
      a = a[attribute].toLowerCase();
      b = b[attribute].toLowerCase();
      if (a < b) return -1;
      if (a > b) return 1;
      return 0;
    }
  }
}

/** Pull in the contents of an external file at the given path. */
function include(path) {
  path = publish.conf.templatesDir+path;
  return IO.readFile(path);
}

/**
 *
 * @param path string Path to template to include
 * @param data hash Data hash to contain all the placeholder names and values
 */
function includeTemplate(path, data) {
  data = data || {};

  //LOG.inform("Including template from "+path+" with params "+data);

  try {
    var template = new JSDOC.JsPlate(publish.conf.templatesDir + path);
    return template.multiProcess(data);
  }
  catch(e) { print(e.message); quit(); }
 
  return '';
}

/** Turn a raw source file into a code-hilited page in the docs. */
function makeSrcFile(path, srcDir, name) {
  if (JSDOC.opt.s) return;
  
  if (!name) {
    name = path.replace(/\.\.?[\\\/]/g, "").replace(/[\\\/]/g, "_");
    name = name.replace(/\:/g, "_");
  }
  
  var src = {path: path, name:name, charset: IO.encoding, hilited: ""};
  
  if (defined(JSDOC.PluginManager)) {
    JSDOC.PluginManager.run("onPublishSrc", src);
  }

  if (src.hilited) {
    IO.saveFile(srcDir, name+publish.conf.ext, src.hilited);
  }
}

/** Build output for displaying function parameters. */
function makeSignature(params) {
  if (!params) return "()";
  var signature = "("
  +
  params.filter(
    function($) {
      return $.name.indexOf(".") == -1; // don't show config params in signature
    }
  ).map(
    function($) {
      return $.name;
    }
  ).join(", ")
  +
  ")";
  return signature;
}

/** Find symbol {@link ...} strings in text and turn into rst links */
function resolveLinks(str, from) {
  str = str.replace(/\{@link ([^} ]+) ?\}/gi,
    function(match, symbolName) {
      return ':js:class:`' + symbolName + '<'+symbolName+'>`';
    }
  );
  
  return str;
}

/**
 * Extend string by providing left trim method
 * Method removes the common left side white space
 *
 * @return Trimmed string
 */
String.prototype.ltrim = function() {
  var text = this;
  var minIndent = 1000;
  var lines = text.toString().split("\n");
  var prespace = /^\s*/;

  // Iterate line to find out minimum indent
  for(var l = 0; l < lines.length; l++) {
    var indent = prespace.exec(lines[l])[0].length;
    if (indent < minIndent) {
      minIndent = indent;
    }
  }

  // Iterate lines of string and remove prefixed space
  for(var s = 0; s < lines.length; s++) {
    lines[s] = lines[s].substring(minIndent)
  }

  return lines.join('\n');
};


/** 
 * Pads spacing in the beginning of
 * the files
 *
 * @param text string line(s)
 * @depth int amount of padding, default is 4
 * @depth bool indent first line or not, default is true
 */
function reIndent(text, depth, indentFirst) {
  depth = typeof depth != "undefined" ? depth : 4;
  indentFirst = typeof indentFirst != "undefined" ? indentFirst : true;

  var lines = text.toString().split("\n");

  // Iterate lines
  for (var l = 0; l < lines.length; l++) {
    var indentedText = '';
    var line = lines[l];

    // Pad space in beginning of each line
    for (var i = 0; i < depth; i++) {
      indentedText += " ";
    }

    // Put padding and text into array and reset indent
    if (!indentFirst && l == 0) {
      lines[l] = line;
    } else {
      lines[l] = indentedText + line;
    }
  }

  return lines.join("\n");
}

/**
 * Simple html to rst Converter
 *
 * @param {String} rawstr HTML string to covert. One or multiple lines
 */
function toRst(rawstr) {
  var rstLines = new Array();

  var lines = rawstr.toString().split("\n");
  for(var l =0; l < lines.length ; l++) {
    var line = lines[l];

    // Remove attribute
    line = line.replace(/\<(\/?\w*)([^\>]*)\>/g, '<$1>');

    // Italic
    line = line.replace(/\<i\>/g, "*");
    line = line.replace(/\<\/i\>/g, "*");

    // Bold
    line = line.replace(/\<.?b\>/g, "**");
    line = line.replace(/\<.?strong\>/g, "**");

    // Code
    line = line.replace(/\<.?code\>/g, "``");
    line = line.replace(/\<.?pre\>/g, "``");

    // Unicode
    line = line.replace('&#64;', '@');

    // Blank row/break
    line = line.replace(/\<br(\s|\/)*\>/g, '\n\n');

    // List
    line = line.replace(/\s*\<.?ul\>/g, '\n\n').trim();
    line = line.replace(/\s*\<li\>/g, '\n* ').trim();
    line = line.replace(/\s*\<\/li\>/g, '\n').trim();

    // eat divs
    // TODO: consider using containers?
    line = line.replace(/\<.?div\>/g, "\n");

    rstLines.push(line);
  }

  return rstLines.join('\n').ltrim();
}

/**
 * Function joins multiple lines
 * into one line, except the ones with separate paragraphs
 */
function reJoin(text) {
  var joinedText = "";

  // TODO: room for improvement?
  text = text.replace(/\n\s*\n/, "<<--NEWLINE-->>");
  var lines = text.toString().split("\n");
  return lines.join(" ").replace("<<--NEWLINE-->>", "\n\n");
}

/**
 * Generates the line from given character, with
 * the same length as the title
 *
 * @param title {String} Title to be underlined
 * @param uchar {String} Underline character or string
 * @param withTitle {boolean} Flag whether return value should have the title or not
 * @returns {String} Underlinining
 */
function underline(title, uchar, withTitle) {
  uchar = uchar || "-";
  withTitle = withTitle || true;
  var line = "";

  for(var l = 0; l<title.length; l++) {
    line += uchar;
  }

  if (withTitle) {
    return title + "\n" + line;
  }
  return line;
}

/**
 * Transforms the given object into JSON and returns it back
 * @param {Object} obj Object to transform into readable format: json
 */
function jsonify(obj) {
  load(JSDOC.opt.t+"/json2.js");
  return JSON.stringify(obj);
}

// Extend string object

String.prototype.underline = function(uchar, withTitle) {
  return underline(this, uchar, withTitle);
};

String.prototype.reJoin = function() {
  return reJoin(this);
};

String.prototype.toRst = function() {
  return toRst(this);
};

String.prototype.reIndent = function(depth, indentFirst) {
  return reIndent(this, depth, indentFirst);
};

/**
 *
 * @param params
 * @param compact
 */
JSDOC.JsPlate.prototype.multiProcess = function(params, compact) {
	var keys = JSDOC.JsPlate.keys;
	var values = JSDOC.JsPlate.values;

  var g = new Object();
  for (var pkey in params) {
    g[pkey] = params[pkey];
  }

	try {
		eval(this.code);
	}
	catch (e) {
		print(">> There was an error evaluating the compiled code from template: "+this.templateFile);
		print("   The error was on line "+e.lineNumber+" "+e.name+": "+e.message);
		var lines = this.code.split("\r");
		if (e.lineNumber-2 >= 0) print("line "+(e.lineNumber-1)+": "+lines[e.lineNumber-2]);
		print("line "+e.lineNumber+": "+lines[e.lineNumber-1]);
		print("");
	}

  // Remove lines that contain only space-characters, usually left by lines in the template
	if (compact) { // patch by mcbain.asm
 		output = output.replace(/\s+?(\r?)\n/g, "$1\n");
 	}

	return output;
};

