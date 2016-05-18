<script type="text/javascript" src="{{url_for('static',filename='jquery.1.8.0.min.js')}}"></script>
<script type="text/javascript" src="{{url_for('static',filename='jquery.form.js')}}"></script>
<!--<script type="text/javascript" src="{{url_for('static',filename='buttondex.js')}}"></script>-->
<script type="text/javascript" src="{{url_for('static',filename='buttondex.js')}}"></script>
voici vos transactions:

{% for transaction in transactions %}
<li>
{% if transaction.etat==0 %}
{{transaction.filehash}} : valider en envoyant 0.0005BTC vers cette adresse {{transaction.bitcoinaddr}}
{% else %}
Transaction valid�e du document {{transaction.filehash}} avec l'id {{transaction.txid}}
{% endif %}
</li>
{% endfor  %}

<script>
$(document).ready(function() {

$( "#envoie" ).click(function() {

  document.location=('/');
});

$( "#recherche" ).click(function() {

  document.location=('/recherche');
});

});
</script>

<input id="envoie" type="submit" value="accueil">

<h4>trouver une transaction a partir du txid</h4>
<input id="recherche" type="submit" value="rechercher">
