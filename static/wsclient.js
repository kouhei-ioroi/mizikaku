var url = "wss://"+window.location.host+"/ws";
var websocket = null;
function init(){open()}
function open(){
  if (websocket == null){
    websocket=new WebSocket(url);
    websocket.onopen=onOpen;
    websocket.onmessage=onMessage;
    websocket.onclose=onClose;
    websocket.onerror=onError;}
    }
function onOpen(event){}
function onMessage(event){
  document.getElementsByName("element_2")[0].value = event.data
}
function onError(event){}
function onClose(event){
  websocket = null;
  open();
}
open()
