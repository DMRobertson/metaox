var log = {
	generic: function(type, message){
		var entry = document.createElement('li')
		entry.className = type
		entry.innerText = message
		game.log.appendChild(entry)
	},
	error:    function(message){ log.generic('error', message) },
	info:     function(message){ log.generic('info',  message) },
	message:  function(message){ log.generic('',      message) },
}

var game = {
	cell_state_names: ["empty", "o", "x"],
};

var main = function(){
	game.log = document.getElementById('log')
	
	game.cells = document.querySelectorAll('.cell')
	for (var i = 0; i < game.cells.length; i++){
		game.cells[i].addEventListener("click", cell_handler, true)
	}
	game.grids = document.querySelectorAll('.metagrid .grid')
	
	game.socket = new WebSocket('ws://' + window.location.hostname + ':8001')
	game.socket.onopen    = socket_connected
	game.socket.onclose   = socket_closed
	game.socket.onerror   = socket_error
	game.socket.onmessage = socket_message
};

var socket_connected = function(e){
	log.info('WebSocket connection established.')
}

var socket_closed = function(e){
	log.info('WebSocket connection closed.')
}

var socket_error = function(e){ 
	log.error('WebSocket error' + e.message)
}

var socket_message = function(e){
	data = JSON.parse(e.data)
	switch (data['type']){
		case 'state':
			log.info('Received update from server')
			apply_state(data)
			break;
		default:
			log.error("Unknown message type: " + data['type'])
	}
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

document.addEventListener("DOMContentLoaded", main, false);