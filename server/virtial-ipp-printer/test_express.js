var fs = require('fs')
var Printer = require('ipp-printer')

var express = require('express')
var app = express()

var config = require('rc')('ipp-printer', {
  name: 'ipp-printer', dir: process.cwd(), port: 3000
})
 
var printer = new Printer(config)

app.all('/', function (req, res) {
	res = 'Good Job!'
})

printer.on('job', function (job) {
  console.log('[job %d] Printing document: %s', job.id, job.name)
 
  var filename = 'job-' + job.id + '-' + Date.now() + '.ps' // .ps = PostScript
  var file = fs.createWriteStream(filename)
 
  job.on('end', function () {
    console.log('[job %d] Document saved as %s', job.id, filename)
  })
 
  job.pipe(file)
})

printer.server.on('listening', function(){
  console.log('Server starts at %s', printer.port)
})

