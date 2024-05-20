
var SCROLL_WIDTH = 24;

var btn_popup = document.getElementById("btn_popup");
var popup = document.getElementById("popup");
var popup_bar = document.getElementById("popup_bar");
var btn_close = document.getElementById("btn_close");
var smoke = document.getElementById("smoke");



console.info("Verificando se o plugin está ativado para ativar o pop-up: ", localStorage.getItem("pluginAtivado"));
if (localStorage.getItem("pluginAtivado")) {

  //-- let the popup make draggable & movable.
  var offset = { x: 0, y: 0 };
  if (popup_bar) {
    popup_bar.addEventListener('mousedown', mouseDown, false);
  }

  window.addEventListener('mouseup', mouseUp, false);

  function mouseUp() {
    window.removeEventListener('mousemove', popupMove, true);
  }

  function mouseDown(e) {
    offset.x = e.clientX - popup.offsetLeft;
    offset.y = e.clientY - popup.offsetTop;
    window.addEventListener('mousemove', popupMove, true);
  }

  function popupMove(e) {
    popup.style.position = 'absolute';
    var top = e.clientY - offset.y;
    var left = e.clientX - offset.x;
    popup.style.top = top + 'px';
    popup.style.left = left + 'px';
  }
  //-- / let the popup make draggable & movable.

  window.onkeydown = function (e) {
    if (e.keyCode == 27) { // if ESC key pressed
      btn_close.click(e);
    }
  }

  /*btn_popup.onclick = function(e){
     // smoke
     spreadSmoke(true);
     // reset div position
     popup.style.top = "4px";
     popup.style.left = "4px";
     popup.style.width = window.innerWidth/2 - SCROLL_WIDTH + "px";
     popup.style.height = window.innerHeight/2 - SCROLL_WIDTH + "px";
    popup.style.display = "block";
   }*/

  window.onresize = function (e) {
    spreadSmoke();
  }



  //--resize---------------------------------

  var element = document.getElementById('popup');
  var resizer = document.createElement('div');
  resizer.className = 'resizer';
  resizer.style.width = '10px';
  resizer.style.height = '10px';
  resizer.style.background = 'rgba(0,0,0,0)';
  resizer.style.position = 'absolute';
  resizer.style.right = 0;
  resizer.style.bottom = 0;
  resizer.style.cursor = 'se-resize';
  element.appendChild(resizer);
  resizer.addEventListener('mousedown', initResize, false);

  function initResize(e) {
    window.addEventListener('mousemove', Resize, false);
    window.addEventListener('mouseup', stopResize, false);
  }
  function Resize(e) {
    element.style.width = (e.clientX - element.offsetLeft) + 'px';
    element.style.height = (e.clientY - element.offsetTop) + 'px';
  }
  function stopResize(e) {
    window.removeEventListener('mousemove', Resize, false);
    window.removeEventListener('mouseup', stopResize, false);
  }


  //resize horizontal e vertical

  // Query the element
  const ele = document.getElementById('popup');

  // The current position of mouse
  let x2 = 0;
  let y2 = 0;

  // The dimension of the element
  let w = 0;
  let h = 0;

  // Handle the mousedown event
  // that's triggered when user drags the resizer
  const mouseDownHandler = function (e) {
    // Get the current mouse position
    x2 = e.clientX;
    y2 = e.clientY;

    // Calculate the dimension of element
    const styles = window.getComputedStyle(ele);
    w = parseInt(styles.width, 10);
    h = parseInt(styles.height, 10);

    // Attach the listeners to `document`
    document.addEventListener('mousemove', mouseMoveHandler);
    document.addEventListener('mouseup', mouseUpHandler);
  };

  const mouseMoveHandler = function (e) {
    // How far the mouse has been moved
    const dx = e.clientX - x2;
    const dy = e.clientY - y2;

    // Adjust the dimension of element
    ele.style.width = `${w + dx}px`;
    ele.style.height = `${h + dy}px`;
  };

  const mouseUpHandler = function () {
    // Remove the handlers of `mousemove` and `mouseup`
    document.removeEventListener('mousemove', mouseMoveHandler);
    document.removeEventListener('mouseup', mouseUpHandler);
  };


  const resizers = ele.querySelectorAll('.resizer');

  // Loop over them
  [].forEach.call(resizers, function (resizer) {
    resizer.addEventListener('mousedown', mouseDownHandler);
  });
}

if (btn_close) {
  btn_close.onclick = function (e) {
    popup.style.display = "none";
    smoke.style.display = "none";
    //limpar elemento sideBar popUp 
    let popUpSideBar = document.querySelector("#popup_sidebar");
    popUpSideBar.innerHTML = '';
  }
}

function spreadSmoke(flg) {
  smoke.style.width = "100%";
  smoke.style.height = "100%";
  smoke.style.left = "0";
  smoke.style.top = "0";
  if (flg != undefined && flg == true) smoke.style.display = "block";
}