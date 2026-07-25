// ==UserScript==
// @name        MDEVs in PRs
// @namespace   https://github.com/vuvova
// @include     https://github.com/MariaDB/server/pull/*
// @include     https://github.com/MariaDB/server/commit/*
// @version     1
// @grant       none
// ==/UserScript==

var spans = document.querySelectorAll('.markdown-title, [class^="CommitHeader-module__commitMessageContainer__"]');
for (var i = 0; i < spans.length; i++) {
  spans[i].innerHTML = spans[i].innerHTML.replace(/MDEV-\d+/g, '<a href="https://jira.mariadb.org/browse/$&">$&</a>');
}
