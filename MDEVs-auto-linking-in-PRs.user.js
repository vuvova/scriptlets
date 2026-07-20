// ==UserScript==
// @name        MDEVs in PRs
// @namespace   https://github.com/vuvova
// @include     https://github.com/MariaDB/server/pull/*
// @version     1
// @grant       none
// ==/UserScript==

var spans = document.getElementsByClassName("markdown-title");
for (var i = 0; i < spans.length; i++) {
  spans[i].innerHTML = spans[i].innerHTML.replace(/MDEV-\d+/g, '<a href="https://jira.mariadb.org/browse/$&">$&</a>');
}
