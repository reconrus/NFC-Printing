Ipp server that is showed as ipp printer.


<H2>INSTALLATION
  
  1. Downdload & Install:
     https://nodejs.org/en/download/
  2. Open Command line in this folder (cmd) or Powershell
  3. Type:
  ```sh 
  npm install
  ```
  4. Copy files 'bind.js', 'printer.js' from "/mod" folder to the "/node_modules/ipp-printer/lib" by replace.
  
 <H2> USAGE
  
   1. Repeat 2d step from installation
   2. Type:
   ```sh
   node main.js
   ```
   3. Server will start at http://localhost:3000
   4. Login: name_en, Password: surname_en (from dbo.data)
   4. Add new printer into your machine by hands as "Microsoft" -> "Microsoft PS Calss Driver"
   5. Use it as a default printer
   6. All documnents that you sent are stored in this folder.
