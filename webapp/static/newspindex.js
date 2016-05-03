'use strict';

var translate = function(x) {
  return x;
};


$(document).ready(function() {
 
var bar = $('.bar');  
  var upload_submit = $('#upload_submit');
  var upload_form = $('#upload_form');
 
  var explain = $('#explain');
  var dropbox = $('.dropbox');

  // uncomment this to try non-HTML support:
  //window.File = window.FileReader = window.FileList = window.Blob = null;

  var html5 = window.File && window.FileReader && window.FileList && window.Blob;
  $('#wait').hide();

  var handleFileSelect = function(f) {
    if (!html5) {
      return;
    }
    var reader = new FileReader();
    reader.onload = function(e) {
      var data = e.target.result;
      setTimeout(function() {
        CryptoJS.SHA256(data, crypto_callback, crypto_finish);
      }, 200);

    };
    
    reader.readAsBinaryString(f);
    show_message(output, 'info');
  };
  if (!html5) {
    explain.html(translate('disclaimer'));
    upload_form.show();
  } else {
    dropbox.show();
    dropbox.filedrop({
      callback: handleFileSelect
    });
    dropbox.click(function() {
      $('#file').click();
    });
  }


 var crypto_callback = function(p) {
    var w = ((p * 100).toFixed(0));
    bar.width(w + '%');
  };
  var crypto_finish = function(hash) {
    bar.width(100 + '%');
    explain.html(translate('Document hash: ') + hash);
	//stop here redirect to /newsavehash/hash which will contain the button
	document.location=('/newsavehash/'+hash);
	// now send 0.0005BTC to this address <address> to save your proof in the blockchain
	//plus a button the click will start the createrawtransaction==>send
	//then we return the txid
 	
  };


  document.getElementById('file').addEventListener('change', function(evt) {
    var f = evt.target.files[0];
    handleFileSelect(f);
  }, false);

  // upload form (for non-html5 clients)
  

  
});

