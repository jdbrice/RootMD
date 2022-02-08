--- 
title: "wow" 
author: "Daniel" 
date: "Hello" 
---

## RootMd Example

This is a simple example of markdown processed by RootMD.
You can include any `c++` code that ROOT can handle. For instance (using ROOT6)

this part of the file was processed with
```sh
rootmd example_in.md -f md -o example.md
```

```cpp
cout << "Hello from ROOT (stdout)" << endl;
cerr << "Hello from ROOT (stderr)" << endl;
```

```cpp
TH1 * h1 = new TH1F( "hGaus", ";x;counts", 100, -5, 5 );
h1->FillRandom( "gaus", 10000 );
h1->Draw( "pe" );
h1->Draw( "same hist" );
gPad->Print( "h1.svg" );
```


$$ 
f(x) = \frac{1}{x}
$$


```css
.svg  {
    width: 100%;
    height: 100%; 
}


div.root-block pre {
    margin-top: 0px!important;
    /* margin-bottom: 0px!important; */
    border-left: 5px solid grey;
    border-right: 5px solid grey;
    border-bottom: 2px solid grey;
    border-top: 2px solid grey;
}

div.root-block-green pre {
    margin-top: 0px!important;
    margin-bottom: 0px!important;

    border-left: 5px solid #64dd17;
    border-right: 5px solid #64dd17;
    /* border-bottom: 2px solid #64dd17; */
    /* border-top: 2px solid #64dd17; */
}

.x3 {
    width:32%;
    display: inline-block;
}
.x2 {
    width:49%;
    display: inline-block;
}
.x4 {
    width:24%;
    display: inline-block;
}
```




```cpp test:value
//input:line-numbers
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
//image: x3
```


```cpp

gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
//image: x2
```

```cpp

gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
gPad->Print( "h1.svg" );
//image: x4
```


```cpp
lets get wrecked
```