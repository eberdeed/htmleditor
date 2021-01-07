"""
   HTMLData: A class to encapsulate the HTML tags as a parallel list.
   Created by Edward Charles Eberle <eberdeed@eberdeed.net>
   December 2015, San Diego, California
"""


class HTMLData:
    """A class to encapsulate the HTML tags as a parallel list. 
    """

    opentags = list(["<!--", "<?php", "<!DOCTYPE","<abbr","<address","<area",\
        "<article","<aside","<audio","<a","<base","<bdi",\
        "<bdo","<blockquote","<body","<br","<button","<b",\
        "<canvas","<caption","<center","<cite","<code","<col",\
        "<colgroup","<data","<datalist","<dd","<del","<details",\
        "<dfn","<dialog","<div","<dl","<dt","<em","<embed",\
        "<fieldset","<figcaption","<figure","<footer","<form",\
        "<h1","<h2","<h3","<h4","<h5","<h6","<head","<header",\
        "<hgroup","<hr","<html","<iframe","<img","<input",\
        "<ins","<i","<kbd","<keygen","<label","<legend","<li",\
        "<link","<main","<map","<mark","<menu","<menuitem",\
        "<meta","<meter","<nav","<noscript","<object","<ol",\
        "<optgroup","<option","<output","<param","<pre","<progress",\
        "<p","<q","<rb","<rp","<rt","<rtc","<ruby","<samp",\
        "<script","<section","<select","<small","<source","<span",\
        "<strong","<style","<sub","<summary","<sup","<s",\
        "<table","<tbody","<td","<template","<textarea","<tfoot",\
        "<th","<thead","<time","<title","<tr","<track","<ul"])    
    
    closetags = list(["-->", "?>", "None", "</abbr>", "</address>", "</area>", "</article>", \
        "</aside>", "</audio>", "</a>", "</base>", "</bdi>", "None", \
        "</blockquote>", "</body>", "None", "</button>", "</b>", "</canvas>", \
        "</caption>", "</center>", "</cite>", "</code>", "</col>", "</colgroup>", \
        "</data>", "</datalist>", "</dd>", "</del>", "</details>", "</dfn>", \
        "</dialog>", "</div>", "</dl>", "</dt>", "</em>", "</embed>", \
        "</fieldset>", "</figcaption>", "</figure>", "</footer>", "</form>", \
        "</h1>", "</h2>", "</h3>", "</h4>", "</h5>", "</h6>", "</head>", \
        "</header>", "</hgroup>", "</hr>", "</html>", "</iframe>", "None", \
        "</input>", "</ins>", "</i>", "</kbd>", "</keygen>", "</label>", \
        "</legend>", "</li>", "None", "</main>", "</map>", "</mark>", \
        "</menu>", "</menuitem>", "None", "</meter>", "</nav>", "</noscript>", \
        "</object>", "</ol>", "</optgroup>", "</option>", "</output>", \
        "</param>", "</pre>", "</progress>", "</p>", "</q>", "</rb>", \
        "</rp>", "</rt>", "</rtc>", "</ruby>", "</samp>", "</script>", \
        "</section>", "</select>", "</small>", "None", "</span>", \
        "</strong>", "</style>", "</sub>", "</summary>", "</sup>", "</s>", \
        "</table>", "</tbody>", "</td>", "</template>", "</textarea>", \
        "</tfoot>", "</th>", "</thead>", "</time>", "</title>", "</tr>", \
        "</track>", "</ul>", "</u>", "</var>", "</video>", "</wbr>"])