# Draw over ROOT


```cpp
TH1 * h = new TH1F( "h", R"F(\sigma \frac{1}{2} P_{\perp})F", 200, -7, 7 );
h->FillRandom( "gaus", 50000 );
h->Draw();
gPad->Print( "gaus.png" );
gPad->Print( "gaus.svg" );
```



```css
.ict {
    width:100%;
    height:100%;
    position: relative;
    text-align: center;
}

.x-label {
    position: absolute;
    bottom: 5%;
    left: 50%;
}

/* Bottom left text */
.bottom-left {
  position: absolute;
  bottom: 8px;
  left: 16px;
}



.centered {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.y-axis-label {
    color: red;
}


```
```html
<div class="ict" >
    <img src="gaus.png"  style="width:100%;"/>
    <div class="bottom-left">Bottom Left</div>
    <div class="centered">WOW Left</div>
    <div class="x-label">Hello there X</div>
</div>
```


```cpp

h->Draw();
gPad->Print("gaus.pdf");
```

# Hello there PDF

```cpp
h->Draw();
gPad->Print("gaus2.ps");
```


# Hello again

