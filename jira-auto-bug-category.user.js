// ==UserScript==
// @name        Jira auto bug category
// @namespace   https://github.com/vuvova
// @include     https://jira.mariadb.org/browse/*
// @version     1
// @grant       none
// ==/UserScript==

var observer = new MutationObserver(function(mutations) {
  resolution=document.getElementById("resolution");
  category=document.getElementById("customfield_13205");
  relnotes=document.getElementById("customfield_13206");
  if (resolution && category && relnotes && category.options[9].text == "Not for Release Notes") {
      resolution.addEventListener('change', function() {
        if (resolution.selectedIndex) {
          category.selectedIndex = 9;
          category.parentNode.style=relnotes.parentNode.style='display:none';
        } else {
           category.selectedIndex = 0;
          category.parentNode.style=relnotes.parentNode.style='display:visible';
        }
    });
  }
});

observer.observe(document.body, { childList: true });
