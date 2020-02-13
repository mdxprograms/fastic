# Fastic

>Flask based static site boilerplate/generator


[![Netlify Status](https://api.netlify.com/api/v1/badges/2b6e7e5a-e314-47b7-be7b-e7d4dfc630e7/deploy-status)](https://app.netlify.com/sites/fastic/deploys)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/mdxprograms/fastic)

### requirements
`python 3`

### setup
```bash
make create-venv && echo "DEBUG=True" > .env
```

### run dev
`make dev`

### run build
`make build`

### Using Collections
If you have a need for collections you can specify the folder within `config.py`

Example: `collections = ['products']`

This will grab all `.md` files within `pages/products` and add them to the
`collections` dict to use in your templates.

Assuming there would be a `title` frontmatter property in a products collection file.
```jinja2
{% for product in collections.products %}
  <h3>{{ product.title }}</h3>
{% endfor %}
```
