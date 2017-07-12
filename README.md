# FinancesApp2
An app designed to help with managing personal finances. The data in this video isn't real bank data.

<img src="Pics/demo.gif">

To use the app you will either have to create some pseudo-data using the data creator code or save your bank data in a folder name "Stats" in the same directory as the main.py file. Currently the app only works with data from TSB bank accounts. However, other banks may be added later.

To create pseudo-data simply set the variable 'demo' to 'on' in the settings file. A wizard will then help you either create new data or use current random data.

Whether using demo data or your own bank data the app has the same set of features. These are shown below, the check boxes without ticks are under development.
- [x] Clean up the bank data to make it more readable by humans (remove nonsense strings, change the case of ALL CAPS words, remove random dates in the description and numbers and unnecessary punctuation)
- [x] Plot and tabulate data
- [ ] Pivots in tables.
- [x] Edit categories within the table.
- [x] Be able to search through data with or without RegEx.
- [x] Plot the spend for each category of data in a bar chart.
- [ ] Be able to save editted data. Not sure if I would want it all saving into 1 document or just updating a current one?
- [x] Categorise data
- [x] Find time averaged incomings and outgoings.
- [ ] Predict future balance, could use the averages to begin with...
- [x] Paypal integration.
- [x] Have a settings page to change things outside of the source code such as the look of the app.
- [ ] Be able to write scripts within the app to perform functions on the data without changing the source code.
- [ ] Be able to download statement data without leaving the app... maybe through a web browser within the app... Not a priority...
- [ ] Be able to load new data into the app.


** Other important features of the code: **

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

Other notes:
  * I want to use Python3 and PyQT 5.
  * I'll be using the Pandas library and Numpy and Matplotlib extensively.
