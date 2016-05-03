
//get the txid from the button
$(document).ready(function() {
$( "#butt" ).click(function() {
txid=($("#zorro").val());

//$.get('./find/' + txid, function(donne){
//	$("#result").text("voici votre hash: "+donne);

$.get('./find/' + txid, function(donne){
	$("#result").text("voici votre hash: "+donne);

});
});
});
