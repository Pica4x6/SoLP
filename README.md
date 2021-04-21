# SoLP


There are three directories files: 

    - Scripts: This is a simplyfied version of our static analysis to check whether an extension is or 
    is not overprivileged. First, there are some dependencies that this files needs to be installed. 
    To execute it, just download the extension (either .zip or .crx) and modify line 411 of SoLP.py with the 
    corresponding name of the file. That file has to be in the same directory as the script. We included some random 
    extensions in the zip as examples. 
    - Extension: Here you can find the first version of the browser extension we will freely distribute in the 
    Web Store. This version does show information to the users in real-time and does not interact with other 
    extensions. To install it, the developer mode has to be enable in Chrome. 
    
    - http: We implemented the web page and will be publicly avaliable. To run it, execute index.html in a web 
    server   

It is remarkable that the data that both the extension and the http contain belong to extensions we crawled months
ago and it is included in the paper. Thus, there might be some mismatch between current extensions and the ones we 
analyzed and can be found here. 
