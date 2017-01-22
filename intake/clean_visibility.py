#!/usr/bin/python3

""" remove invisible text from .html files by inspecting <div>s with display:none css style """

import sys
import os
import io

def clean_visibility( folder, fileName ):
    print(fileName)

    fin = open( folder + fileName, encoding='utf-8' )
    fout = open( folder + 'clean/' + fileName, 'w', encoding='utf-8' )

    text = fin.read()
    fin.close()

    fout.write( cleaned( text ) )
    fout.close()

def cleaned( text ):
    """ run though text as state machine """
    with io.StringIO() as output:

        # a quick state machine
        in_tag = False
        started_div_tag = False
        in_div_content = False
        write_output = True
        skip_one = False # sometimes we ask output to skip over just one char
        kill_div = False

        tag_sb = [] # string builder: detect tag starting
        div_tag_sb = [] # accumulate div tag text (when excising)
        content_sb = [] # accumulate div internal content (for controlling what is excised)

        for c in text:
            skip_one = False

            if c == '<':
                in_tag = True
                write_output = False

            if in_tag:
                curr_tag = u''.join(tag_sb).lower()

                if c == ' ':
                    if curr_tag == '<div':
                        if not kill_div:
                            started_div_tag = True
                            print('.', end='')
                        else:
                            print('kill mode: waiting for /div')

                if c == '>':
                    if started_div_tag:
                        # check if this div interests us
                        if "style='display:none;'" in curr_tag:
                            kill_div = True
                            in_div_content = True
                            div_sb = tag_sb
                            div_sb.append(c)
                        else:
                            write_output = True
                            output.write( u''.join(tag_sb) )

                        started_div_tag = False
                    else:
                        if kill_div:
                            if curr_tag == '</div':
                                print( ':', end='') #"/DIV/ REMOVED: " +  u''.join(content_sb) + c )
                                content_sb = []
                                div_tag_sb = []
                                kill_div = False
                                skip_one = True
                                in_div_content = False
                        else:
                            #print("tag: "+ curr_tag)
                            output.write( u''.join(tag_sb) )

                    if not kill_div:
                        write_output = True

                    in_tag = False
                    tag_sb = []

            if in_tag:
                tag_sb.append(c)

            if in_div_content:
                content_sb.append(c)

            if write_output and not skip_one:
                output.write(c)

        return output.getvalue()

def process_all_files( folder, extension = '.html'):
    os.makedirs( folder+'clean/', exist_ok = True )
    files = [ f for f in os.listdir(folder) if f.endswith(extension) ]
    for f in files:
        clean_visibility(folder, f)

if len(sys.argv) == 2:
    process_all_files(sys.argv[1])

else:
    """ testing """

    text_test = """<div class='panta-doc-npk' style='display:none;'>2</div><DIV class='TV213'  ><a name='p1'></a><a class='p_id' name='p-2680'></a><P class='TV213 TVP' id='p1'><b>1.</b> Latvija.</P><div class='panta-doc-npk' style='display:none;'>2</div><div id='panta-piezime-2680' class='panta-piezimite'></div></DIV>
    <DIV class='TV213'  ><a name='p2'></a><a class='p_id' name='p-2681'></a><P class='TV213 TVP' id='p2'><b>2.</b> Latvijas.</P><div class='panta-doc-npk' style='display:none;'>3</div><div id='panta-piezime-2681' class='panta-piezimite'></div></DIV>"""

    text_orig = "<div class='panta-doc-npk' style='display:none;'>2</div><DIV class='TV213'  ><a name='p1'></a><a class='p_id' name='p-2680'></a><P class='TV213 TVP' id='p1'><b>1.</b> Latvija.</P><div class='panta-doc-npk' style='display:none;'>2</div><div id='panta-piezime-2680' class='panta-piezimite'></div></DIV><DIV class='TV213'  ><a name='p2'></a><a class='p_id' name='p-2681'></a><P class='TV213 TVP' id='p2'><b>2.</b> Latvijas.</P><div class='panta-doc-npk' style='display:none;'>3</div><div id='panta-piezime-2681' class='panta-piezimite'></div></DIV>";

    text_expect = "<DIV class='TV213'  ><a name='p1'></a><a class='p_id' name='p-2680'></a><P class='TV213 TVP' id='p1'><b>1.</b> Latvija.</P><div id='panta-piezime-2680' class='panta-piezimite'></div></DIV><DIV class='TV213'  ><a name='p2'></a><a class='p_id' name='p-2681'></a><P class='TV213 TVP' id='p2'><b>2.</b> Latvijas.</P><div id='panta-piezime-2681' class='panta-piezimite'></div></DIV>";

    text_res = cleaned(text_orig)
    print( "======= "+ text_res )
    if text_res == text_expect:
        print("MATCHED")
    else:
        print("**NO MATCH**")
