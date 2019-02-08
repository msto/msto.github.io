---
layout: page
title: Lecture notes
permalink: /notes/
---

{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}

Notes from classes I've taken.

{% for semester in site.semesters %}
# {{semester}}
{% for class in site.classes %}
{% if class.semester == semester %}
  [{{class.course}}]({{ site.baseurl }}{{ class.url }})
{% endif %}
{% endfor %}
{% endfor %}
