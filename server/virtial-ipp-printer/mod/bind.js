'use strict'

var util = require('util')
var os = require('os')
var http = require('http')
var Bonjour = require('bonjour')
var ipp = require('ipp-encoder')
var debug = require('debug')(require('../package').name)
var groups = require('./groups')
var operations = require('./operations')

var auth = require('http-auth');
var sql = require('mssql');
var userId = -1;

var config = {
    server: 'localhost',
    database: 'test_skip_card',
    user: 'user',
    password: 'kQzYxVJMt8l5O8P51r0YdHHc',
    port: 1433
};

var basic = auth.digest({
		realm: "Simon Area."
	}, (username, password, callback) => {
	    // Custom authentication
	    // Use callback(error) if you want to throw async error.
		//callback(username === "user" && password === "user");
    //var key = authentication(username, password, config);
    var dbConn = new sql.Connection(config);

    var authKey= false;
    //5.
    dbConn.connect().then(function () {
        //6.
        var request = new sql.Request(dbConn);
        //7.
        request.query(`select name_en,surname_en,Card_ID from data WHERE name_en = '${username}' `).then(function (recordSet) {
            //console.log(recordSet);

            if (recordSet.length!=0 && password == recordSet[0].surname_en){
                    authKey = true;
                    userId = recordSet[0].Card_ID;
                    //console.log("password correct");

                  }
            callback(authKey);

            dbConn.close();

        }).catch(function (err) {
            //8.
            console.log(err);
            dbConn.close();
            return false;
        });
    }).catch(function (err) {
        //9.
        console.log(err);
        return false;
    });


	}
);


var C = ipp.CONSTANTS

module.exports = function (printer) {
  var server = printer.server
  var bonjour = Bonjour()

  if (server) {
    server.on('request', onrequest)
    if (server.address()) onlistening()
    else server.on('listening', onlistening)
  } else {
    server = printer.server = http.createServer(basic, onrequest)
    server.listen(printer.port, onlistening)
  }

  return printer

  function onrequest (req, res) {
    debug('HTTP request: %s %s', req.method, req.url)

    if (req.method !== 'POST') {
      res.writeHead(405)
      res.end()
      return
    } else if (req.headers['content-type'] !== 'application/ipp') {
      res.writeHead(400)
      res.end()
      return
    }

    req.on('data', consumeAttrGroups)
    req.on('end', fail)

    function consumeAttrGroups (chunk) {
      req._body = req._body ? Buffer.concat([req._body, chunk]) : chunk

      try {
        req._body = ipp.request.decode(req._body)
      } catch (e) {
        debug('incomplete IPP body - waiting for more data...')
        return
      }

      req.removeListener('data', consumeAttrGroups)
      req.removeListener('end', fail)

      printer.emit('operation', req._body)
      router(printer, req, res)
    }

    function fail () {
      // decode only the most essential part of the IPP request header to allow
      // best possible response
      if (req._body.length >= 8) {
        var body = {
          version: { major: req._body.readInt8(0), minor: req._body.readInt8(1) },
          operationId: req._body.readInt16BE(2),
          requestId: req._body.readInt32BE(4)
        }
      }
      send(printer, body, res, C.CLIENT_ERROR_BAD_REQUEST)
    }
  }

  function onlistening () {
    printer.port = server.address().port
    printer.userId = userId;

    if (!printer.uri) printer.uri = 'ipp://' + os.hostname() + ':' + printer.port + '/'

    debug('printer "%s" is listening on %s', printer.name, printer.uri)
    printer.start()

    if (printer._zeroconf) {
      debug('advertising printer "%s" on network on port %s', printer.name, printer.port)
      bonjour.publish({ type: 'ipp', port: printer.port, name: printer.name })
    }
  }
}

function router (printer, req, res) {
  var body = req._body
  printer.userId = userId;
  debug('IPP/%d.%d operation %d (request #%d)',
    body.version.major,
    body.version.minor,
    body.operationId,
    body.requestId,
    util.inspect(body.groups, { depth: null }))

  res.send = send.bind(null, printer, body, res)

  if (body.version.major !== 1) return res.send(C.SERVER_ERROR_VERSION_NOT_SUPPORTED)

  switch (body.operationId) {
    // Printer Operations
    case C.PRINT_JOB: return operations.printJob(printer, req, res)
    case C.VALIDATE_JOB: return operations.validateJob(printer, req, res)
    case C.GET_PRINTER_ATTRIBUTES: return operations.getPrinterAttributes(printer, req, res)
    case C.GET_JOBS: return operations.getJobs(printer, req, res)

    // Job Operations
    case C.CANCEL_JOB: return operations.cancelJob(printer, req, res)
    case C.GET_JOB_ATTRIBUTES: return operations.getJobAttributes(printer, req, res)

    default: res.send(C.SERVER_ERROR_OPERATION_NOT_SUPPORTED)
  }
}

function send (printer, req, res, statusCode, _groups) {
  printer.userId = userId;
  if (typeof statusCode === 'object') return send(printer, req, res, C.SUCCESSFUL_OK, statusCode)
  if (statusCode === undefined) statusCode = C.SUCCESSFUL_OK

  var obj = {}
  if (printer.fallback && req && req.version.major === 1 && req.version.minor === 0) obj.version = { major: 1, minor: 0 }
  obj.statusCode = statusCode
  obj.requestId = req ? req.requestId : 0
  obj.groups = [groups.operationAttributesTag(ipp.STATUS_CODES[statusCode])]
  if (_groups) obj.groups = obj.groups.concat(_groups)

  debug('responding to request #%d', obj.requestId, util.inspect(obj, { depth: null }))

  var buf = ipp.response.encode(obj)

  res.writeHead(200, {
    'Content-Length': buf.length,
    'Content-Type': 'application/ipp'
  })

  res.end(buf)
}




////// HTTP-AUTH Events //////

basic.on('success', (result, req) => {
	console.log(`User authenticated: ${result.user}`);
});

basic.on('fail', (result, req) => {
	console.log(`User authentication failed: ${result.user}`);
});

basic.on('error', (error, req) => {
	console.log(`Authentication error: ${error.code + " - " + error.message}`);
});
