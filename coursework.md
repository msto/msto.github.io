---
layout: page
title: Coursework
permalink: /coursework/
---

{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}

Lecture notes and projects from courses I've taken.

{% for semester in site.semesters %}
# {{semester}}
{% for course in site.coursework %}
{% if course.semester == semester %}
  [{{course.number}} &ndash; {{course.title}}]({{ site.baseurl }}{{ course.url }})
{% endif %}
{% endfor %}
{% endfor %}
