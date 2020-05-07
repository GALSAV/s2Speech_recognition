/*

	Rzye Tello
	
	Scratch Ext 1.0.0.0

	http://www.ryzerobotics.com

	1/1/2018
*/

var dataToTrack_keys = ["battery", "x", "y", "z", "speed"];
var lastDataReceived = null;


var http = require('http');
var fs = require('fs');
var url = require('url');

var osdData = {};

var PORT = 8889;
var HOST = '192.168.10.1';

var PORT2 = 8890;
var HOST2 = '0.0.0.0';

var dgram = require('dgram');
var client = dgram.createSocket('udp4');

const server = dgram.createSocket('udp4');

var message = new Buffer( 'command' );
client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
	if (err) {
		throw err;
	}
});

http.createServer( function (request, response) {  


	/*if(command != 'poll')
	{
		var message = new Buffer( 'command' );
		client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
			if (err) {
				console.log(err);
				throw err;
			}
		});		
	}	*/	

	var pathname = url.parse(request.url).pathname;
       
    var url_params = request.url.split('/');

    if (url_params.length < 2)
        return;

    var command = url_params[1];
	
	  switch (command){
		
        case 'poll':
            respondToPoll(response);
            break;
		
        case 'takeoff':
			console.log('takeoff');
			TakeoffRequest();
		break;
		
        case 'land':
			console.log('land');
			LandRequest();
		break;
		
        case 'up':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('up ' + dis);
			var message = new Buffer( 'up '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});
		break;

        case 'down':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('down ' + dis);
			var message = new Buffer( 'down '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});			
		break;

        case 'left':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('left ' + dis);
			var message = new Buffer( 'left '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});
		break;

        case 'right':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('right ' + dis);
			var message = new Buffer( 'right '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});
		break;		
		
		case 'forward':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('forward ' + dis);
			var message = new Buffer( 'forward '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});			
		break;		
		
        case 'back':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('back ' + dis);
			var message = new Buffer( 'back '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});			
		break;

        case 'cw':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('cw ' + dis);
			var message = new Buffer( 'cw '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});
		break;

		case 'flip':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('flip' + dis);
			var message = new Buffer( 'flip '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});			
		break;	

		case 'ccw':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('ccw ' + dis);
			var message = new Buffer( 'ccw '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;	
			});
			client.on('message',function(msg,info){
				console.log('Data received from server : ' + msg.toString());
				console.log('Received %d bytes from %s:%d\n',msg.length, info.address, info.port);
			});								
		break;		
		
		case 'setspeed':
			dis = (url_params.length >= 3) ? url_params[2] : 0;
			console.log('setspeed ' + dis);
			var message = new Buffer( 'speed '+ dis );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});			
		break;	

			
	  }
	response.end('Hello Tello.\n');
   
}).listen(8001);


console.log('---------------------------------------');
console.log('Tello Scratch Ext running at http://127.0.0.1:8001/');
console.log('---------------------------------------');


function respondToPoll(response){

    var noDataReceived = false;
/*
    var resp = "";
    var i;
    for (i = 0; i < dataToTrack_keys.length; i++){
        resp += dataToTrack_keys[i] + " ";
        resp += (i+10);
		resp += "\n";
    }
	console.log('resp : ' + resp);*/

	let rst = '';
	for(let k in osdData) {
		rst += `${k} ${osdData[k]}\n`;
	}
	//console.log('rst : ' + rst);
    response.end(rst);
	client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
	if (err) {
		throw err;
	}
}

function TakeoffRequest(){
	
	var message = new Buffer('command');

	client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
		if (err) throw err;
	});
	var message = new Buffer('takeoff');
	client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
		if (err) throw err;

	});
}

function LandRequest(){

	var message = new Buffer('land');

	client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
		if (err) throw err;
	});
}

let listenState = function () 
{
	var message = new Buffer( 'command' );
			client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
				if (err) throw err;
			});			
/*	server.on('message', (msg, rinfo) => 
	{ 	msg = msg.toString().trim();
		let fieldList = msg.split(';');
		console.log({fieldList});
		fieldList.forEach(function (field){let [key, value] = field.split(':');osdData[key] = value; console.log('key={key} value={value}')})
	});

	server.on('listening', () => {const address = server.address();console.log(`server listening ${address.address}:${address.port}`);});

	server.bind(PORT2, HOST2);*/
	console.log('listenState'); 
	server.on('error', (err) => {
	  console.log(`server error:\n${err.stack}`);
	  server.close();
	});

	server.on('message', (msg, rinfo) => {
	  console.log(`server got: ${msg} from ${rinfo.address}:${rinfo.port}`);
	});

	server.on('listening', () => {
	  const address = server.address();
	  console.log(`server listening ${address.address}:${address.port}`);
	});
	server.bind({
		address: '192.168.10.2',
		port: 8890,
		exclusive: true
	});
};

//listenState();


