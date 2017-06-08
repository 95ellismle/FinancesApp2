# FinancesApp2
A new version of the original finances app found on my profile. 

I haven't got much of it written yet but the core aims of it are readability of code, the interface should be designed with aesthetics in mind (but obviously not sacrifice functionality) and the code should be object orientated.

To begin with the app will be built for Ubuntu. However, if I have the inclination later I may try to get it working for Windows as well depending on whether anyone else would want to use it!


Readability
  * The code should be commented well, with a standard style used consistently throughout.
  * Functions should be explained in one or two lines above the function.
  * Performance can probably be sacrificed for readability (and definitely functionality). The app will be using bank data, so the     size of the data frames will be fairly easy for an average to handle with inefficient code.
  * The code should be object orientated! Functions can be kept outside of the main code in a seperate file.

Aesthetics:
  * The look and feel of the interface is important, the previous app looked like it came with Windows 95!
  * Less is more in terms of design.
  * Use big bold colour, like google's material desgin... Use a colour pallette that matches!
  * Keep things as tidied away as possible.
  
Functionality:
   * Plot and tabulate data (the table should be interactive this time with pivots)
   * Have all the usual search functionality of the old app.
   * Be able to save editted data. Not sure if I would want it all saving into 1 document or just a part of it?
   * Categorise data (maybe try to improve the categorisation. Machine learning  may eventually help, far in the future)
   * Find time averaged income -Specify an amount of days and have it tell me how much money I spend on average in that time.
   * Find time averaged outgoings.
   * Predict future balance, could use the averages to begin with...
   * Paypal integration.
   * Have a settings page to change things outside of the source code such as the look of the app.
   * Be able to write scripts within the app to perform on the data without changing the source code.
   * Be able to download statement data without leaving the app... maybe through a web browser within the app...
     
Other notes:
  * I want to use Python3 and PyQT 5.
  * I'll be using the Pandas library and Numpy and Matplotlib extensively.




# Currently:
The app is currently still in its infancy. I have some basic code to categorise the bank data, a GUI to display the data from accounts in separate tabs. The code is fully object orientated and hopefully much more readable than the previous (spaghetti code) attempt. I have a separate file for back-end functions in the Data folder. This contains functions which can parse data from text files into dictionaries, categorise the data and read/save data etc... The Gui/front-end stuff is currently kept in the Gui folder. At the moment this is only a Table Widget to display the bank data.
