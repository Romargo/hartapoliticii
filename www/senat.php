<?
// If you are accessing this page directly, redirect to the front page
if (!$DB_USER) {
  header('Location: http://www.vivi.ro/politica');
}


$title = "Senat, mandatul 2004-2008";
include('header.php');

printWarning();
?>

<div class="plaintext">Pentru prezență, am luat în calcul cele 750 de voturi electronice din Senat exercitate
între Septembrie 2007 și Noiembrie 2008.
</div>

<?

//include('functions_deprecated.php');
//computeSenatePresenceAggregates();

showSenatePresencePercentage($_GET['sort'], $_GET['order']);
?>
