// game state

var game = {
	cell_state_names: ["empty", "o", "x", "drawn"],
	handlers: {}
}

// ui references

var ui = {
	elements: {},
	handlers: {},
	util: {}
}

//logging etc

var log = {
	generic: function(type, message){
		var entry = document.createElement('li')
		entry.className = type
		entry.textContent = message
		var log = ui.elements.log
		log.appendChild(entry)
		log.scrollTop = log.scrollHeight
	},
	debug:    function(message){ log.generic('debug', message) },
	error:    function(message){ log.generic('error', message) },
	info:     function(message){ log.generic('info',  message) },
	message:  function(message){ log.generic('',      message) },
}

// websocket handlers

var socket_connected = function(e){ log.info('Connected to server.') }
var socket_closed    = function(e){ log.error('Lost connection to server: code ' + e.code) }
var socket_error     = function(e){ log.error('Unspecified WebSocket error.') }
var socket_message = function(e){
	log.debug(e.data)
	data = JSON.parse(e.data)
	for (var key in data){
		if (data.hasOwnProperty(key)){
			handler = game.handlers[key]
			if (handler === undefined){
				log.error('No handler for ' + key + ': ' + JSON.stringify(data[key]))
			} else {
				handler(data[key])
			}
		}
	}
}

// game state handlers

game.handlers.active = function(coords){
	for (var n = 0; n < ui.elements.grids.length; n += 1){
		ui.elements.grids[n].classList.remove("active")
	}
	var n = 3 * coords[0] + coords[1]
	ui.elements.grids[n].classList.add("active")
}

game.handlers.chat = function(message){
	log.generic('chat', message)
}

game.handlers.client_names = function(clients){
	for (var i = 0; i < ui.elements.clients.length; i += 1){
		var input = ui.elements.clients[i]
		var li = input.parentElement
		if (i < clients.length){
			var pos = input.selectionStart
			input.value = clients[i]
			input.selectionStart = input.selectionEnd = pos
			li.classList.remove('unused')
		} else {
			li.classList.add('unused')
			li.classList.remove('x')
			li.classList.remove('o')
		}
	}
	log.debug('Updated client list')
}

game.handlers.grids = function(grids){
	for (var key in grids){
		if (grids.hasOwnProperty(key)){
			var i = grids[key][0]
			var j = grids[key][1]
			for (var n = 0; n < 9; n += 1){
				var k = Math.floor(n / 3)
				var l = n % 3
				cell = document.getElementById('cell'+i+j+k+l)
				ui.util.remove_cell_classes(cell)
				cell.classList.add(game.cell_state_names[grids[key][n+2]])
			}
		}
	}
}

game.handlers.metagrid = function(cells){
	for (var k = 0; k < 9; k += 1){
		var i = k % 3
		var j = Math.floor(k / 3)
		var grid = ui.elements.grids[k]
		ui.util.remove_cell_classes(grid)
		grid.classList.add(game.cell_state_names[cells[k]])
	}
}

game.handlers.my_id = function(id){
	for (var i = 0; i < ui.elements.clients.length; i += 1){ 
		var input = ui.elements.clients[i]
		var li = input.parentElement
		li.classList.remove('me')
		input.disabled = true
	}
	var me = ui.elements.clients[id]
	me.parentElement.classList.add('me')
	me.disabled = false
}

// ui handlers 
ui.handlers.cell = function(e){
	var cell = e.target
	var grid = cell.parentElement.parentElement.parentElement
	if (cell.classList.contains("empty") && grid.classList.contains("active")){
		id = cell.id.substring(4)
		game.socket.transmit('mark', id)
	}
}

ui.handlers.chat = function(e){
	if (e.keyCode !== 13){
		return
	}
	var text = e.target.value
	var r = /^\/([A-Za-z][A-Za-z_]*)(?: (.+)$)?/
	match = text.match(r)
	if (match !== null){
		if (match[2] === undefined){
			match[2] = ''
		}
		game.socket.transmit(match[1], match[2])
	} else {
		game.socket.transmit('say', text)
	}
	e.target.value = ''
}

ui.handlers.chat_blur =  function(e){
	if (e.target.value === ''){
		e.target.value = 'Send a message...'
	}
}
ui.handlers.chat_focus = function(e){
	if (e.target.value === 'Send a message...'){
		e.target.value = ''
	}
}

ui.handlers.on_rename = function(e){
	game.socket.transmit('edit_name', e.target.value)
}

// ui utility functions 

ui.util.remove_cell_classes = function(element){
	for (key in game.cell_state_names){
		if (game.cell_state_names.hasOwnProperty(key)){
			element.classList.remove(game.cell_state_names[key])
		}
	}
}

// setup 

var main = function(){
	prepare_elements()
	
	game.socket = new WebSocket('ws://' + window.location.hostname + ':8001')
	game.socket.onopen    = socket_connected
	game.socket.onclose   = socket_closed
	game.socket.onerror   = socket_error
	game.socket.onmessage = socket_message
	game.socket.transmit  = function(command, arg){
		msg = command + ' ' + arg
		log.debug('-> ' + msg)
		game.socket.send(msg)
	}
};

var prepare_elements = function(){
	ui.elements.cells = document.querySelectorAll('.cell')
	for (var i = 0; i < ui.elements.cells.length; i++){
		ui.elements.cells[i].addEventListener("click", ui.handlers.cell)
	}
	
	ui.elements.chat = document.querySelector('#chat')
	ui.elements.chat.addEventListener('keypress', ui.handlers.chat)
	ui.elements.chat.addEventListener('focus'   , ui.handlers.chat_focus)
	ui.elements.chat.addEventListener('blur'    , ui.handlers.chat_blur)
	//IE and Firefox do not reset the value of input elements when the page is refreshed.
	ui.elements.chat.value = ''
	//force a blur event
	ui.elements.chat.focus()
	ui.elements.chat.blur()
	
	ui.elements.clients = document.querySelectorAll('#clients input')
	for (var i = 0; i < ui.elements.clients.length; i += 1){
		ui.elements.clients[i].addEventListener('input', ui.handlers.on_rename)
	}
	
	ui.elements.grids = document.querySelectorAll('#metagrid .grid')
	
	ui.elements.log = document.getElementById('log')
	
	ui.elements.metagrid = document.getElementById('#metagrid')
}

document.addEventListener("DOMContentLoaded", main, false);