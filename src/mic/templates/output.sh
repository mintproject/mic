{% if compress -%}
zip {{ compress }} {{ files|join(' ') }}
{% endif %}
