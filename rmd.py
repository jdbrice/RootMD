#!/usr/bin/env conda run -n py38 python

import mistletoe as md2
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.base_renderer import BaseRenderer
"""
HTML renderer for mistletoe with ROOT code execution and asset injection.
"""
# import pdb
import re
import html
import os
import select
from subprocess import Popen, PIPE
import base64
from shutil import copyfile
import sys

print( "NOW", flush=True )

TITLE = "rootmd"
EMBED = False
ASSET_DIR = ""
ASSET_PREFIX = ""
prismjs = """<script src="{}"></script>\n""".format( "https://cdnjs.cloudflare.com/ajax/libs/prism/1.26.0/prism.min.js" )
prismcss = """<link href="{}" rel="stylesheet" />\n""".format( "https://cdnjs.cloudflare.com/ajax/libs/prism/1.26.0/themes/prism-tomorrow.min.css" )
prismajs = '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.26.0/plugins/autoloader/prism-autoloader.min.js" integrity="sha512-GP4x8UWxWyh4BMbyJGOGneiTbkrWEF5izsVJByzVLodP8CuJH/n936+yQDMJJrOPUHLgyPbLiGw2rXmdvGdXHA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>'

doct = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{title}</title>
    
    {head}

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto" rel="stylesheet"> 
    
    <style>
    html {{
        font-family: 'Roboto', sans-serif;
    }}

    .content {{
            max-width: 90%;
            margin: auto;
        }}
    @media (min-width:1200px) {{
        .content {{
            max-width: 75%;
        }}
    }}

    @media (min-width:1900px) {{
        .content {{
            max-width: 60%;
        }}
    }}

    .png {{
        display: inline-block;
        margin-left: auto;
        margin-right: auto;
        max-width: 100%;
    }}

    pre {{
        font-size: 0.9em!important;
        line-height: 0.9!important;
    }}

    </style>
  </head>
  <body>
    <div class="content" >
    {body}
    </div>
  </body>
</html>"""

codetemplate = '<pre class="languag-{lang}"><code class="language-{lang}">{inner}</code></pre>'
divtemplate = '<div class="output" >' + codetemplate + '</div>'
imgtemplate = '<img src="{src}" class="png"/>'




class RootRenderer(HTMLRenderer):
    def __init__(self, *extras):
        super().__init__(*extras)
        # pdb.set_trace()
        self.p = Popen(['root', '-l', '-b'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        # capture any of that initial stuff ROOT prints out
        self.run_root( "" )
        self.blockid = 0
    
    def read_available(self, s, time_limit=0):
        output = ""
        while True:
            poll_result = select.select([s], [], [], time_limit)[0]
            if len(poll_result) > 0 :
                l = s.readline()
                if ( "ROOTEOF" in l ):
                    return output
                output += l
            elif time_limit != None:
                break
        return output
    def run_root( self, code ):
        code_lines = [ l + '\n\r' for l in code.splitlines()]
        code_lines.append( 'cout << "ROOTEOF" << endl;\r' ) # needed to signal end of read, else deadlock
        code_lines.append( 'cerr << "ROOTEOF" << endl;\r' ) # needed to signal end of read, else deadlock
        self.p.stdin.writelines( code_lines )
        output = self.read_available( self.p.stdout, None)
        err = self.read_available( self.p.stderr, None)
        # print( ">\n%s" % output )
        # print( ">\n%s" % err )

        # get image names from output to cerr
        imgs = []
        for m in re.findall( "file *(.*) *has", err ):
            imgs.append(m)
        return (output, err, imgs)
    
    def process_image_output(self, path):
        path = path.strip()
        _, ext = os.path.splitext( path )
        ext = ext.replace( ".", "" )

        if ASSET_DIR != "" and not EMBED:
            print( "cp %s %s" % (path, ASSET_DIR) )
            copyfile( path, ASSET_DIR )

        if EMBED:
            with open(path, "rb") as image_file:
                b64_encoded = base64.b64encode(image_file.read())
                template = '<img src="data:image/{ext};charset=utf-8;base64,{data}" class="{cls}"/>'

                if "svg" == ext:
                    ext = "svg+xml"

                return template.format( ext=ext, data=b64_encoded.decode(), cls=ext )
        else:
            return "\n" + imgtemplate.format( src=path )

    def render_block_code(self, token):
        # print( "CODE_BLOCK")
        code_block = super().render_block_code(token)
        code =token.children[0].content
        if token.language:
            attr = ' class="{}"'.format('language-{}'.format(self.escape_html(token.language)))
        else:
            attr = ''
        if "cpp" == self.escape_html(token.language) :
            if "//noexec" in code:
                return code_block

            output, err, imgs = self.run_root( code )
            output = ("# Block [%d]\n" % self.blockid) + output

            # CONTROL OPTIONS
            if "noout" in code:
                output = ""
            if "noerr" in code:
                err = ""
            if "quiet" in code or "//q" in code:
                output = ""
                err = ""
            if "//qin" in code:
                code_block = "" # dont output the code
            
            # inject stdoutput 
            divout = '<div id="{id}" class="root-output" style="text-align: center;">'.format( id="root-output-%d" % (self.blockid) )
            if len( output + err ):
                divout += "\n" + divtemplate.format( lang="sh", inner=self.escape_html(output + err) )
            divout += '</div>'

            # inject images
            imgout = '<div id="{id}" class="root-images" style="text-align: center;">'.format( id="root-images-%d" % (self.blockid) )
            for i in imgs:
                imgout += self.process_image_output( i )
            imgout += '</div>'

            if "//qimg" in code or "//!img" in code:
                imgout = ""

            self.blockid = self.blockid + 1
            return code_block + divout + imgout
        
        if "js" == token.language:
            template = '<script>\n{content}\n</script>'
            if "//qin" in code:
                code_block = "" # dont output the code
            if "//noexec" in code:
                return code_block
            return code_block + template.format(content=code)
        if "css" == token.language:
            template = '<style>\n{content}\n</style>'
            if "//qin" in code or "/*qin*/" in code:
                code_block = "" # dont output the code
            return code_block + template.format(content=code)
        if "html" == token.language:
            template = '<div>\n{content}\n</div>'
            if "<!--qin-->" in code or "<!-- qin -->" in code:
                code_block = "" # dont output the code
            if "<!--noexec-->" in code or "<!-- noexec -->" in code:
                return code_block
            return code_block + template.format(content=code)

        return code_block
        
    def render_document(self, token):
        self.footnotes.update(token.footnotes)
        inner = '\n'.join([self.render(child) for child in token.children])
        return doct.format( title=TITLE, head=(prismjs + prismcss + prismajs), body= '\n\n{}\n'.format(inner) if inner else '' )


class RootMdRenderer(BaseRenderer):
    def __init__(self, *extras):
        # pdb.set_trace()
        super().__init__(*extras)
        print("SPAWN ROOT")
        self.p = Popen(['root', '-l', '-b'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
        print("INIT START")
        self.run_root( "" )
        print("INIT DONE")
        self.blockid = 0
    
    def read_available(self, s, time_limit=0):
        # print( "READ_AVAILABLE" )
        output = ""
        while True:
            # print("BEFORE POLL")
            poll_result = select.select([s], [], [], time_limit)[0]
            if len(poll_result) > 0 :
                # print( "pol_result", poll_result)
                l = s.readline()
                if ( "ROOTEOF" in l ):
                    return output
                output += l
            elif time_limit != None:
                break
        return output

    def run_root( self, code ):
        code_lines = [ l + '\n\r' for l in code.splitlines()]
        code_lines.append( 'cout << "ROOTEOF" << endl;\r' )
        code_lines.append( 'cerr << "ROOTEOF" << endl;\r' )
        self.p.stdin.writelines( code_lines )
        output = self.read_available( self.p.stdout, None)
        err = self.read_available( self.p.stderr, None)
        # print( ">\n%s" % output )
        # print( ">\n%s" % err )

        imgs = []
        for m in re.findall( "file *(.*) *has", err ):
            imgs.append(m)
        return (output, err, imgs)

    def process_image_output(self, path):
        path = path.strip()
        _, ext = os.path.splitext( path )
        ext = ext.replace( ".", "" )
        template = '![{src}]({src})'

        if ASSET_DIR != "" and not EMBED:
            print( "cp %s %s" % (path, os.path.join(ASSET_DIR, path ) ) )
            copyfile( path, os.path.join(ASSET_DIR, path ) )

        if EMBED:
            with open(path, "rb") as image_file:
                b64_encoded = base64.b64encode(image_file.read())
                template = '![{text}](data:image/{ext};charset=utf-8;base64,{data})'
                
                if "svg" == ext:
                    ext = "svg+xml"
                return template.format( ext=ext, data=b64_encoded.decode(), text=_ )
        else:
            npath = path
            if ASSET_PREFIX != "":
                npath = os.path.join( ASSET_PREFIX, os.path.basename(path) )
                print( "rewriting asset path: %s -> %s" % ( path, npath ) )
            return "\n" + template.format( src=npath )

    def render_block_code(self, token):
        # print( "CODE_BLOCK")
        template = """```{lang}\n{content}\n```\n"""
        

        code =token.children[0].content
        output = template.format( lang = token.language if token.language else '', content= token.children[0].content )
        if not token.language or token.language != "cpp":
            return output

        if "//noexec" in code:
            return output

        routput, err, imgs = self.run_root( code )

        output = template.format( lang = token.language if token.language else '', content= token.children[0].content )


        output += template.format( lang="sh", content=( ("# Block [%d]\n" % self.blockid) + routput + err) )

        # inject images
        imgout = ""
        for i in imgs:
            imgout += self.process_image_output( i )
        self.blockid = self.blockid + 1
        return output + imgout
    
    @staticmethod
    def render_line_break(token):
        return '\n' if token.soft else '\n'

    def render_to_plain(self, token):
        if hasattr(token, 'children'):
            inner = [self.render_to_plain(child) for child in token.children]
            return ''.join(inner)
        return (token.content)

    def render_heading(self, token):
        inner = self.render_inner(token)
        out = "#" * int(token.level) + " " + inner
        return out

    def render_document(self, token):
        inner = '\n'.join([self.render(child) for child in token.children])
        return inner

import argparse
# from os.path import exists

parser = argparse.ArgumentParser(description='Convert Markdown with inline c++ code to ROOT output.')
parser.add_argument('input', help='Markdown file')
parser.add_argument('-o', '--output', help='output filename  default <in>.html', default="")
parser.add_argument('-f', '--format', help='output format', default="html", choices=["html", "md", "obsidian"])
parser.add_argument('-e', '--embed', help='embed images as base 64', default=False, action="store_true")
parser.add_argument('-a', '--asset-dir', help='specify asset output directory, paths are NOTE re-written to support unless using obsidian format', default="")

args = parser.parse_args()
print(args)

exts = {
    "html" : ".html",
    "md"   : ".md",
    "obsidian" : ".md"
}
print( "MAIN", flush=True )
sys.stdout.flush()
EMBED = args.embed
ASSET_DIR = args.asset_dir
if args.output == "":
    args.output = args.input  + exts[args.format]# ext will be added later

basename = os.path.basename( args.output )

# handle obsidian's way of removing the attachment/ (or whatever dir) from paths
if args.format == "obsidian":
    ASSET_PREFIX = os.path.splitext(basename)[0]
    ASSET_DIR = os.path.join( ASSET_DIR, ASSET_PREFIX )
    if not os.path.isdir( ASSET_DIR ):
        print( "Making asset directory: %s" % ASSET_DIR )
        os.mkdir( ASSET_DIR )

if os.path.exists(args.input) :
    print( "Processing %s to %s output format" % (args.input, args.format ) )
    TITLE = args.input
    theRenderer = RootRenderer
    if args.format == "md" or args.format == "obsidian":
        theRenderer = RootMdRenderer
    with open( args.input , 'r') as fin:
        with theRenderer() as renderer:
            html = renderer.render(md2.Document(fin))

    output = args.output
    if "" == output :
        output = args.input + "." + args.format

    print( "Writing output to %s" % output )
    with open( output , "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)
else:
    print("File %s does not exist" % ( args.input ) )