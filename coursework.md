---
layout: page
title: Coursework
permalink: /coursework/
---

{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}

Lecture notes and projects from courses I've taken.

Any inaccuracies or incompleteness in scribe notes should be attributed to me
and not considered reflective of the lecturer.

{% for semester in site.semesters %}
# {{semester}}
{% for course in site.coursework %}
{% if course.semester == semester %}
  [{{course.number}} &ndash; {{course.title}}]({{ site.baseurl }}{{ course.url }})
{% endif %}
{% endfor %}
{% endfor %}
