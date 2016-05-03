$(document).ready(function() {

$( "#envoie" ).click(function() {

  $.get('../savehash/' + {{hash}}, function(data){
	$("#result").text("votre checksum a ete enregisté avec le txid: "+data);

});
});
});
