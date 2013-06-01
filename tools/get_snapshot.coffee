page = require("webpage").create()
address = undefined
page.onConsoleMessage = (msg) ->
  console.log msg

if phantom.args.length is 0
  console.log "Usage: get_snapshot.js <some URL>"
  phantom.exit()
else
  address = phantom.args[0]
  page.open address, (status) ->
    if status isnt "success"
      console.log "FAIL to load the address"
    else
      fs = require "fs"
      results = page.evaluate ->
        doc = document.documentElement.innerHTML

        return doc.substring(doc.indexOf("<svg"), doc.indexOf("</svg") + 6);

      date = new Date().toISOString().replace(/:/g, "-")#
      fs.write('snapshot-'+date+'.svg', results ,'w');

    phantom.exit()

