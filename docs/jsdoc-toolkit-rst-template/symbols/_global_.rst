==================================
livvkit.resources.js.common module
==================================

.. contents::
   :local:

.. js:data:: _global_

   .. ============================== constructor details ====================
   
   .. ============================== properties summary =====================
   
   .. ============================== events summary ========================
   
   .. ============================== field details ==========================
   
   .. ============================== method details =========================
   
   .. js:function:: drawNav()
   
       Draws the navigation sidebar by looking at the index.json data and appends the
       list of resultant pages to the nav div.
   
   .. js:function:: drawContent()
   
       Draws content to the page by looking at the name of the page and loading the
       appropriate dataset.
   
   
   .. js:function:: drawSummary(data, div)
       
       :param Object data:
   
         - The data representing the summary.  Determined by data["Type"] = "Summary"
   
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a summary and adds it to the div.
   
   .. js:function:: drawValSummary(data, div)
       
       :param Object data:
   
         - The data representing the summary.  Determined by data["Type"] = "Summary"
       
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a validation extension summary and adds it to the div.
   
   .. js:function:: drawError(data, div)
       
       :param Object data:
   
         - The error element data.  Determined by having data["Type"] = "Error"
       
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build an error message and appends it to the div.
   
   .. js:function:: drawDiff(data, div)
       
       :param Object data:
   
         - The data representing the table.  Determined by data["Type"] = "Diff"
       
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a file diff
   
   .. js:function:: drawBitForBit(data, div)
       
       :param Object data:
   
         - The data representing the table.  Determined by
           data["Type"] = "Bit for Bit"
       
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a bit for bit table
   
   .. js:function:: drawTable(data, div)
   
       :param Object data:
   
         - The data representing the table.  Determined by data["Type"] = "Table"
       
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a table
   
   .. js:function:: drawVTable(data, div)
       
       :param Object data:
   
         - The data representing the table.  Determined by data["Type"] = "Vertical Table"
   
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a vertical table
   
   .. js:function:: drawGallery(data, div)
   
       :param Object data:
   
         - The data representing the table.  Determined by data["Type"] = "Gallery"
   
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Build a gallery
   
   .. js:function:: drawImage(data, div)
       
       :param Object data:
   
         - The data representing the table.  Determined by data["Type"] = "Image"
       
       :param string div:
   
         - The name of the div to draw to.  Should be referenced as a string that
           determines whether it is a class or id (ie include # or .)
   
       Draw an image
   
   .. js:function:: drawThumbnail(path, size)
       
       :param string path:
   
         - The location of the image to thumbnail-ize
       
       :param number size:
   
         - The desired height to draw
   
       Draw an image thumbnail with a link to open in a new tab
       
       :returns:
         the html to embed into another element
   
   .. js:function:: loadJSON(path)
       
       :param  path:
   
       Load a json file into a variable
   
   .. ============================== event details =========================
   
.. container:: footer

   Documentation generated by jsdoc-toolkit_  2.4.0 using jsdoc-toolkit-rst-template_

.. _jsdoc-toolkit: http://code.google.com/p/jsdoc-toolkit/
.. _jsdoc-toolkit-rst-template: http://code.google.com/p/jsdoc-toolkit-rst-template/
.. _sphinx: http://sphinx.pocoo.org/

.. vim: set ft=rst :
