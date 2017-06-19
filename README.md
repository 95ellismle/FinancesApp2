# FinancesApp2
A new version of the original finances app found on my profile. 

I haven't got much of it written yet but the core aims of it are readability of code, the interface should be designed with aesthetics in mind (but obviously not sacrifice functionality) and the code should be object orientated.

To begin with the app will be built for Ubuntu. However, if I have the inclination later I may try to get it working for Windows as well depending on whether anyone else would want to use it!


Readability of the Code:
  * The code should be commented well, keep it concise but informative.
  * Functions should be explained in one or two lines above the function.
  * Use built-in functions and library functions! These will be faster, easier to read, and more stable than anything I write!
  * The code should be object orientated. Functions can be kept outside of the main code in a seperate file. Use classes for Widgets, keep it tidy!
  * Files should be sensibly named, i.e Table for the code relating to the Table.

Aesthetics:
  * The look and feel of the interface is important, the previous app looked like it came with a dodgy version of Windows 95!
  * Use simple non contrasting colours so as to not distract from the functionality. Must look modern and 'up-to-date'!
  * Keep things as tidied away as possible. Less is definitely more!
  * Use CSS to style the app, any pages of pure, undynamic text should be written in HTML.
  * Styling should be consistent throughout, use the same background colour for all widgets etc... 
  * Use minimal adornments on widgets. E.g. tables don't need gridlines, widgets don't need borders, graphs don't need matplotlib's silly frame!
  * Key points are simplicity and readability.
  
Functionality:
- [x] Plot and tabulate data 
- [ ] Add pivots to the table.
- [ ] Edit categories within the table.
- [x] Be able to search through data using RegEx.
- [x] Plot the spend for each category of data.
- [ ] Be able to save editted data. Not sure if I would want it all saving into 1 document or just updating a current one?
- [x] Categorise data 
- [x] Find time averaged incomings and outgoings.
- [ ] Predict future balance, could use the averages to begin with...
- [ ] Paypal integration.
- [ ] Have a settings page to change things outside of the source code such as the look of the app.
- [ ] Be able to write scripts within the app to perform functions on the data without changing the source code.
- [ ] Be able to download statement data without leaving the app... maybe through a web browser within the app... Not a priority...
   
Other notes:
  * I want to use Python3 and PyQT 5.
  * I'll be using the Pandas library and Numpy and Matplotlib extensively.



