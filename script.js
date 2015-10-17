//logging etc

var log = {
	generic: function(type, message){
		var entry = document.createElement('li')
		entry.className = type
		entry.innerText = message
		game.elements.log.appendChild(entry)
	},
	debug:    function(message){ log.generic('debug', message) },
	error:    function(message){ log.generic('error', message) },
	info:     function(message){ log.generic('info',  message) },
	message:  function(message){ log.generic('',      message) },
}

var socket_connected = function(e){ log.info('WebSocket connection established.') }
var socket_closed    = function(e){ log.info('WebSocket connection closed.')      }
var socket_error     = function(e){ log.error('WebSocket error' + e.message)      }

// game state

var game = {
	cell_state_names: ["empty", "o", "x"],
	elements: {},
	handlers: {}
}

// io

var socket_message = function(e){
	data = JSON.parse(e.data)
	log.debug(JSON.stringify(data))
	type = data['type']
	try {
		game.handlers[type](data)
	} catch (e) {
		log.error("Error: " + e.message)
		log.error(JSON.stringify(data))
	}
}

// handlers

game.handlers.client_names = function(data){
	var clients = data['clients']
	for (var i = 0; i < clients.length; i += 1){
		game.elements.clients[i].innerText = clients[i] 
		game.elements.clients[i].classList.remove('me')
	}
	for (; i < game.elements.clients.length; i += 1){
		game.elements.clients[i].innerText = ''
		game.elements.clients[i].classList.remove('me')
	}
	game.elements.clients[data['my_id']].classList.add('me')
	log.debug('Updated client list')
}

var apply_state = function(data){
	for (var i = 0; i < game.grids.length; i++){
		game.grids[i].classList.remove("active")
		set_cell_state(game.grids[i], data['grids'][i])
	}
	i = data['active'][0] + 3 * data['active'][1]
	game.grids[i].classList.add("active")
	
	for (var i = 0; i < game.cells.length; i++){
		set_cell_state(game.cells[i], data['board'][i])
	}
}

var cell_handler = function(e){

}

var set_cell_state = function (element, state){
	if (typeof state === "number"){
		state = game.cell_state_names[state]
	}
	switch (state){
		case 'x':
			element.classList.add("x")
			element.classList.remove("o")
			break;
		case 'o':
			element.classList.add("o")
			element.classList.remove("x")
			break;
		case 'empty':
			element.classList.remove("x")
			element.classList.remove("o")
			break;
		default:
			throw new Error("Unrecognised state: " + state)
	}
}

var main = function(){
	game.elements.log = document.getElementById('log')
	
	game.elements.cells = document.querySelectorAll('.cell')
	for (var i = 0; i < game.elements.cells.length; i++){
		game.elements.cells[i].addEventListener("click", cell_handler, true)
	}
	game.elements.grids = document.querySelectorAll('.metagrid .grid')
	game.elements.clients = document.querySelectorAll('#clients li')
	
	game.socket = new WebSocket('ws://' + window.location.hostname + ':8001')
	game.socket.onopen    = socket_connected
	game.socket.onclose   = socket_closed
	game.socket.onerror   = socket_error
	game.socket.onmessage = socket_message
};

document.addEventListener("DOMContentLoaded", main, false);