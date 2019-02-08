---
layout: page
title: Lecture notes
permalink: /notes/
---

{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
{% for class in site.classes %}
  [{{class.title}}]({{ site.baseurl }}{{ class.url }})
{% endfor %}
