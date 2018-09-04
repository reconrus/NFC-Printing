'use strict'

var md5 = require('md5')
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
var MSSQLConnector = require( "node-mssql-connector" );
var userId = -1;

var MSSQLClient = new MSSQLConnector( {
    settings: {
        max: 20,
        min: 0,
        idleTimeoutMillis: 30000,
        detailerror: true
    },
    connection: {
        userName: "user",
        password: "kQzYxVJMt8l5O8P51r0YdHHc",
        server: "localhost",
        options: {
            database: "test_skip_card"
        }
    }
})


//Config of connection to MSSQL Server
//It could be moved into some extern file for useability
var config = {
    server: 'localhost',
    database: 'test_skip_card',
    user: 'user',
    password: 'kQzYxVJMt8l5O8P51r0YdHHc',
    port: 1433
};

//Authentication by 'http-auth'
var digest = auth.digest({
    realm: "Simon Area."

    //Danya & Ilia начинать исправлять отсюда

  }, (username, callback) => {
    // Expecting md5(username:realm:password) in callback.

    //callback(md5(username+ ":Simon Area.:pass"));
    //MSSQL Connector
    var query = MSSQLClient.query( "select surname_en, Card_ID from data WHERE name_en = @username ")
    query.param( "username", "VarChar",  username );
    query.exec( function( err, res ){
    if( err ){
        concole.error( " Query ERROR ")
        console.error( err );
        return
    }

    //console.log(res);

    //Бля я хуй знает как кетчить это
    //Тема такая что если юзер неправильно что-то вводит, надо кетчить ошибку, что не находит поле "surname_en"
    var password = "";

    try{
        console.log(res);
        userId = res.result[0]["card_id"];
        password = res.result[0]["surname_en"];
        console.log(username+ " : " + userId+" : "+password);
        callback(md5(username +":Simon Area.:"+ res.result[0]["surname_en"]));

    }catch( err ){

      console.log(`Didn't find that username: ${username}`+ err);
      callback();

    }





    });

    //Не работает

  });





var C = ipp.CONSTANTS

module.exports = function (printer) {
  var server = printer.server
  var bonjour = Bonjour()

  if (server) {
    server.on('request', onrequest)
    if (server.address()) onlistening()
    else server.on('listening', onlistening)
  } else {             //We append 'digest' as parameter of createServer() for Authentication
    server = printer.server = http.createServer(digest, onrequest)
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

digest.on('success', (result, req) => {
  console.log(`User authenticated: ${result.user}`);
});

digest.on('fail', (result, req) => {
  console.log(`User authentication failed: ${result.user}`);
});

digest.on('error', (error, req) => {
  console.log(`Authentication error: ${error.code + " - " + error.message}`);
});

MSSQLClient.on( "error", function( error ){
    console.log("[ERROR] MSSQL Connector");// handle error
} );
