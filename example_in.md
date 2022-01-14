## Example

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

```cpp
TH1 * h1 = new TH1F( "hGaus", ";x;counts", 100, -5, 5 );
h1->FillRandom( "gaus", 10000 );
h1->Draw( "pe" );
h1->Draw( "same hist" );
gPad->Print( "h1.svg" );
```