import re
import os 
"""
Credit for idea and regexes:  gilles-betrand.com. 
"""

def applyRegexps(text, listRegExp):
    """ Applies successively many regexps to a text"""
    # apply all the rules in the ruleset
    for element in listRegExp:
        left = element['left']
        right = element['right']
        r=re.compile(left)
        text=r.sub(right,text)
    return text

def remove_preamble(text):
    doc_w_end = text.split('\\begin{document}')[1]
    doc = doc_w_end.split('\\begin{thebibliography}')[0]
    return doc

def detex(latexText):
    """Transform a latex text into a simple text"""    
    # initialization
    regexps=[]
    text = remove_preamble(latexText)
    # remove all the contents of the header, ie everything before the first occurence of "\begin{document}"
    text = re.sub(r"(?s).*?(\\begin\{document\})", "", text, 1)

    # remove comments
    regexps.append({r'left':r'([^\\])%.*', 'right':r'\1'})
    text= applyRegexps(text, regexps)
    regexps=[]

    # - replace some LaTeX commands by the contents inside curly rackets
    to_reduce = [r'\\emph', r'\\textbf', r'\\textit', r'\\text', r'\\IEEEauthorblockA', r'\\IEEEauthorblockN', r'\\author', r'\\caption',r'\\author',r'\\thanks']
    for tag in to_reduce:
        regexps.append({'left':tag+r'\{([^\}\{]*)\}', 'right':r'\1'})
    text= applyRegexps(text, regexps)
    regexps=[]

    # - replace some LaTeX commands by the contents inside curly brackets and highlight these contents
    to_highlight = [r'\\part[\*]*', r'\\chapter[\*]*', r'\\section[\*]*', r'\\subsection[\*]*', r'\\subsubsection[\*]*', r'\\paragraph[\*]*']

    # highlightment pattern: #--content--#
    for tag in to_highlight:
        regexps.append({'left':tag+r'\{([^\}\{]*)\}','right':r'\n#--\1--#\n'})

    # highlightment pattern: [content]
    to_highlight = [r'\\title',r'\\author',r'\\thanks',r'\\cite', r'\\ref']
    for tag in to_highlight:
        regexps.append({'left':tag+r'\{([^\}\{]*)\}','right':r'[\1]'})
    text= applyRegexps(text, regexps)
    regexps=[]

    # remove LaTeX tags
    # - remove completely some LaTeX commands that take arguments
    to_remove = [r'\\maketitle',r'\\footnote', r'\\centering', r'\\IEEEpeerreviewmaketitle', r'\\includegraphics', r'\\IEEEauthorrefmark', r'\\label', r'\\begin', r'\\end', r'\\big', r'\\right', r'\\left', r'\\documentclass', r'\\usepackage', r'\\bibliographystyle', r'\\bibliography',  r'\\cline', r'\\multicolumn']
    # replace tag with options and argument by a single space
    for tag in to_remove:
        regexps.append({'left':tag+r'(\[[^\]]*\])*(\{[^\}\{]*\})*', 'right':r' '})
    text= applyRegexps(text, regexps)
    regexps=[]
    # - replace some LaTeX commands by the contents inside curly rackets
    # replace some symbols by their ascii equivalent
    #- common symbols
    regexps.append({'left':r'\\&','right':r'&'})
    regexps.append({'left':r'\\%','right':r'%'})
    
    # - special letters
    regexps.append({'left':r'\\\'{?\{e\}}?','right':r'é'})
    regexps.append({'left':r'\\`{?\{a\}}?','right':r'à'})
    regexps.append({'left':r'\\\'{?\{o\}}?','right':r'ó'})
    regexps.append({'left':r'\\\'{?\{a\}}?','right':r'á'})

    # keep untouched the contents of the equations
    # regexps.append({'left':r'\$(.)\$', 'right':r'\1'})
    # regexps.append({'left':r'\$([^\$]*)\$', 'right':r'\1'})

    # remove the equation symbols ($)
    # regexps.append({'left':r'([^\\])\$', 'right':r'\1'})

    # correct spacing problems
    regexps.append({'left':r' +,','right':r','})
    regexps.append({'left':r' +','right':r' '})
    regexps.append({'left':r' +\)','right':r'\)'})
    regexps.append({'left':r'\( +','right':r'\('})
    regexps.append({'left':r' +\.','right':r'\.'})    

    # remove lonely curly brackets    
    regexps.append({'left':r'^([^\{]*)\}', 'right':r'\1'})
    regexps.append({'left':r'([^\\])\{([^\}]*)\}','right':r'\1\2'})
    regexps.append({'left':r'\\\{','right':r'\{'})
    regexps.append({'left':r'\\\}','right':r'\}'})

    # strip white space characters at end of line
    regexps.append({'left':r'[ \t]*\n','right':r'\n'})

    # remove consecutive blank lines
    regexps.append({'left':r'([ \t]*\n){3,}','right':r'\n'})

    # apply all those regexps
    text= applyRegexps(text, regexps)
    regexps=[]    
    
    text = text.replace('\\mathbbR','\mathbb{R}')
    text = text.replace('\\mathbbQ','\mathbb{Q}')
    text = text.replace('\\mathbbZ','\mathbb{Z}')
    text = text.replace('\\mathbbC','\mathbb{C}')

    # return the modified text
    return text


def detex_folder(path):
    os.chdir(path)
    directory = os.listdir() 
    output_txt = []
    i = 0
    for txt_file in directory:
        print(f'Detexing {i} of {len(directory)}: "{txt_file}"')
        with open(txt_file, 'r') as f:
            content = f.read()
            f.close()
        output_txt.append(detex(content))
        i += 1
    output_txt = ''.join(output_txt)

    name = 'detexified_txt.txt'
    print(f'Saving detexified text to: "{name}"')
    with open(name, 'w+') as output_file:
        output_file.write(output_txt)
        output_file.close()
