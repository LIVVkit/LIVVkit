"""
The TexHelper module provides capabilities to convert LIVVkits output
from JSON to tex files.  It does not convert the tex files to any finished
output.   For example, if you want a PDF you will still have to pass the 
tex files through pdflatex.
"""
import os
import glob
import pprint

import livvkit
from livvkit.util import functions

def write_tex():
    """
    Finds all of the output data files, and writes them out to .tex 
    """
    datadir = livvkit.index_dir 
    outdir = os.path.join(datadir, "tex")
    print(outdir)
    #functions.mkdir_p(outdir)
    
    data_files = glob.glob(datadir + "/**/*.json", recursive=True)
    
    for each in data_files:
        data = functions.read_json(each)
        tex = th.translate_page(data)
        outfile = os.path.join(outdir, os.path.basename(each).replace('json', 'tex'))
        with open(outfile, 'w') as f:
            f.write(tex)


def translate_page(data):
    """
    Translates data elements with data['Type'] = 'page'.  This is the
    top level of translation that occurs, and delegates the translation
    of other element types contained on a page to their proper functions.
    """
    if "Page" != data["Type"]:
        return ""

    tex_str =  (
r'''
\documentclass{article} 
\usepackage{placeins}
\title{LIVVkit}
\author{$USER}
\begin{document}
\maketitle
'''.replace('$USER', livvkit.user)
)                  

    content = data["Data"]
    for tag_name in ["Elements", "Tabs"]:
        for tag in content.get(tag_name, []):
                print("Translating " + tag["Type"])
                tex_str += translate_map[tag["Type"]](tag)
 
    tex_str += (
r'''
\end{document}
'''
)
    return tex_str


def translate_section(data):
    sect_str = ""
    elements = data.get("Elements", [])
    for elem in elements:
            print("    Translating " + elem["Type"])
            sect_str += translate_map[elem["Type"]](elem)
    return sect_str


def translate_tab(data):
    tab_str = ""
    sections = data.get("Sections", [])
    for section in sections:
            print("  Translating " + section["Type"])
            tab_str += translate_map[section["Type"]](section)
    return tab_str


def translate_summary(data):
    headers = sorted(data.get("Headers", []))
    summary = '\\FloatBarrier \n \\section{$NAME} \n'.replace('$NAME', data.get("Title", "table"))
    summary += '\\begin{table} \n \\begin{center}'
    
    # Set the number of columns
    n_cols = len(headers)
    col_str = "l" + "c"*(n_cols)
    summary += '\n \\begin{tabular}{$NCOLS} \n'.replace("$NCOLS", col_str)
    spacer =  ' &' * n_cols + r'\\[.5em]'
    
    for header in headers:
        summary += '& $HEADER '.replace('$HEADER', header).replace('%', '\%')
    summary += ' \\\\ \hline \n'
    
    names = sorted(data.get("Data", []).keys())
    for name in names:
        summary += '\n\n \\textbf{$NAME} $SPACER \n'.replace('$NAME', name).replace('$SPACER', spacer)
        cases = data.get("Data", []).get(name, {})
        for case, c_data in cases.items():
            summary += ' $CASE & '.replace('$CASE', str(case))
            for header in headers:
                h_data = c_data.get(header, "")
                if list is type(h_data) and len(h_data) == 2:
                    summary += (' $H_DATA_0 of $H_DATA_1 &'
                                .replace('$H_DATA_0', str(h_data[0]))
                                .replace('$H_DATA_1', str(h_data[1]))
                                .replace('%', '\%'))
                else:
                    summary += ' $H_DATA &'.replace('$H_DATA', str(h_data)).replace('%','\%')

            # This takes care of the trailing & that comes from processing the headers.  
            summary = summary[:-1] + r' \\'
    
    summary += '\n \end{tabular} \n \end{center} \n \end{table}\n'
    return summary 


def translate_table(data):
    headers = sorted(data.get("Headers", []))
    table = '\\FloatBarrier \n \\section{$NAME} \n'.replace('$NAME', data.get("Title", "table"))
    table += '\\begin{table} \n \\begin{center}'
    
    # Set the number of columns
    n_cols = "c"*(len(headers)+1)
    table += '\n \\begin{tabular}{$NCOLS} \n'.replace("$NCOLS", n_cols)
     
    # Put in the headers
    for header in headers:
        table += ' $HEADER &'.replace('$HEADER', header).replace('%', '\%')
    table = table[:-1] + ' \\\\ \n \hline \n'

    # Put in the data
    for header in headers:
        table += ' $VAL &'.replace("$VAL", str(data["Data"][header])) 
    table = table[:-1] + ' \\\\ \n \hline'
    table += '\n \end{tabular} \n \end{center} \n \end{table}\n'
    return table


def translate_bit_for_bit(data):
    headers = sorted(data.get("Headers", []))
    table = '\\FloatBarrier \n \\section{$NAME} \n'.replace('$NAME', data.get("Title", "table"))
    table += '\\begin{table} \n \\begin{center}'
    # Set the number of columns
    n_cols = "c"*(len(headers)+1)
    table += '\n \\begin{tabular}{$NCOLS} \n'.replace("$NCOLS", n_cols)
   
    # Put in the headers
    table += " Variable &"
    for header in headers:
        table += ' $HEADER &'.replace('$HEADER', header).replace('%', '\%')
    table = table[:-1] + ' \\\\ \n \hline \n'

    # Put in the data
    for k, v in data.get("Data", []).items():
        table += "\n \\textbf{$VAR} & ".replace("$VAR", k)
        for header in headers:
            table += ' $VAL &'.replace("$VAL", str(v[header])) 
        table = table[:-1] + ' \\\\'
    table += '\n \hline \n \end{tabular} \n \end{center} \n \end{table}\n'
    return table


def translate_gallery(data):
    return ""


def translate_image(data):
    return ""


def translate_file_diff(data):
    diff = '\\FloatBarrier \section{Configuration}'
    sections = data.get('Data')
    for title, config in sections.items():
        title = title.replace('_', '\_')
        diff += ' \n \\subsection{$NAME}'.replace('$NAME', title)
        for opt, vals in config.items():
            opt = opt.replace('_', '\_')
            diff += '\n\n \\texttt{$NAME} : '.replace('$NAME', opt)
            if vals[0]:
                diff += '$NAME'.replace('$NAME', vals[-1])
            else:
                diff += ('$NAME1 \\textit{$NAME2}'.replace('$NAME1', vals[1])
                                                      .repace('$NAME2',  vals[-1]))
    diff += '\n\n'
    return diff


def translate_error(data):
    return ""


# Map element types to translations
translate_map = {
           "Summary"     : translate_summary,
           "Section"     : translate_section,
           "Tab"         : translate_tab,
           "Table"       : translate_table,
           "Bit for Bit" : translate_bit_for_bit,
           "Gallery"     : translate_gallery,
           "Image"       : translate_image,
           "Diff"        : translate_file_diff,
           "Error"       : translate_error
       }   


def main():
   write_tex() 

if __name__ == "__main__":
    main()

