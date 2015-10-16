var main = function(){
	var cells = document.querySelectorAll('.cell')
	console.log(cells)
	for (var i = 0; i < cells.length; i++){
		cells[i].addEventListener("click", cell_handler, true)
	}
};

var cell_handler = function(e){
	var cls = e.srcElement.classList
	if (cls.contains("x")){
		set_state(e.srcElement, 'o')
	} else if (cls.contains("o")){ 
		set_state(e.srcElement, 'empty')
	} else {
		set_state(e.srcElement, 'x')
	}
}

var set_state = function (cell, state){
	switch (state){
		case 'x':
			cell.innerText = '\u2717'
			cell.classList.add("x")
			break;
		case 'o':
			cell.innerText = '\u25EF'
			cell.classList.add("o")
			break;
		case 'empty':
			cell.innerText = ''
			cell.classList.remove("x")
			cell.classList.remove("o")
			break;
		default:
			throw new Error("Unrecognised state")
	}
}

document.addEventListener("DOMContentLoaded", main, false);
