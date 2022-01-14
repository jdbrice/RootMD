
# RootMD 🩺 👩🏼‍⚕️

RootMD is a markdown processor for markdown with ROOT-flavored c++ code. RootMD can execute c++ code and inject the output (from stdout, stderr) and link or embed image outputs. Provides a format for producing code + result for better documentation / notes. This is by design not a jupyter notebook, e.g. not a REPL-like environment. If you like Jupyter notebooks then use that :). 

## Features
- execute c++ code blocks via ROOT REPL
- capture stdout, stderr and inject into output
- embed (base64) or link to any image files produced 
- output to HTML or Markdown (or obsidian flavored markdown)
- execute html, css, javascript code blocks (for html output) to customize output file

## usage
```sh
rootmd [-h] [-o OUTPUT] [-f {html,md,obsidian}] [-e] [-a ASSET_DIR] input

    input : the markdown file to process

    -o : specify output file, default is <input>.<format> (for obsidian format the ext is 'md')

    -f : output format
        - html : output to a single html file
        - md : output to generic markdown
        - obsidian : output to markdown, but re-write attachment links to use obsidian style attachment directory
    
    -e : embed image assets as base64 in the output file

    -a : specify asset directory to which the output image files are copied

```


## TODO
- make it a python package (so that it can be installed via pip)
- add watch functionality for reprocessing a file on change
- test some failure modes when root code has errors leading to hang
- add mathjax to html output for inline mathematics
- "import" source files into output? So that you can write code in separate file but sow it in the output?
- support for other "languages", e.g. shell
- support for ROOTJS in HTML output

## Dependencies
RootMD itself is a pure python package which uses:
- mistletoe : python markdown parser and processor
- prismjs for syntax highlighting in HTML output
- ROOT (installed on system and available on PATH)

## Example : see [example_in.md](example_in.md) and [example.md](example.md)
This is a simple example of markdown processed by RootMD.
You can include any c++ code that ROOT can handle. For instance (using ROOT6)
this part of the file was processed with
```sh
rootmd example_in.md -f md -o example.md

```

```cpp
cout << "Hello from ROOT (stdout)" << endl;
cerr << "Hello from ROOT (stderr)" << endl;

```
```sh
# Block [0]
Hello from ROOT (stdout)
Hello from ROOT (stderr)

```

```cpp
TH1 * h1 = new TH1F( "hGaus", ";x;counts", 100, -5, 5 );
h1->FillRandom( "gaus", 10000 );
h1->Draw( "pe" );
h1->Draw( "same hist" );
gPad->Print( "h1.svg" );

```
```sh
# Block [1]
Info in <TCanvas::MakeDefCanvas>:  created default TCanvas with name c1
Info in <TCanvas::Print>: SVG file h1.svg has been created

```

![h1.svg](h1.svg)