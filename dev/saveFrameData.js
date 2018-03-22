// csgomagic json variables to check what the frame contents are
var DATA = new String();
var count = '"onlineCount"';
var ocsg = '"ocsg"';
var chat = 'chat';
var oct = '"oct"';
var oce = '"oce"';
var ocs = '"ocs"';


var BEG = false;

// This replaces the browser's `webSocketFrameReceived` code with the original code
SDK.NetworkDispatcher.prototype.webSocketFrameReceived = function (requestId, time, response) {
  var networkRequest = this._inflightRequestsById[requestId];
  if (!networkRequest) return;
  var frame = response.payloadData;
  if (BEG == false) {
    if (frame.indexOf(ocsg) != -1) {
        BEG = true;
        DATA = DATA + Date.now() + '\n';
    }
  }
  else {
    if (frame.indexOf(oce) != -1) {
        BEG = false;
        DATA = DATA + frame.substring(2) + '\n';
        console.save(DATA, 'scraped_frames.txt');
        DATA = new String();
    }

    else if ((frame.indexOf(oct) == -1) && (frame.indexOf(count) == -1) && (frame.indexOf(chat) == -1) && (frame != 3) && (frame.indexOf(ocs) == -1)) {
        DATA = DATA + frame.substring(2) + '\n';
    }
  }
  networkRequest.addFrame(response, time, false);
  networkRequest.responseReceivedTime = time;
  this._updateNetworkRequest(networkRequest);
}