# Aurora

Aurora is a minimalist, blog-aware static site generator. It only provides the
absolute minimum required to render your Markdown and Jinja templates to a
complete website. Aurora is designed for people who want control over their
content; *your site, your rules.*

Quick help:
```
Aurora - a minimalist, blog-aware static site generator

usage:
    aurora create <project_name>
    aurora new <post_title>
    aurora build

options:
    -h --help  Show this screen.
    --version  Show version.
```

## Installation

Install with pip. Note that only Python 3 is supported.

```
$ pip3 install aurora
```

## Quick start

We will create a very simple blog in this section. Use the `create` command to
scaffold a new directory containing an empty Aurora site.

```
$ aurora create <project_name>
```

There are two primary content type in Aurora: pages and posts. Pages are for
standalone content such as the home or about page while posts are for blogging.

`cd` into the directory and add a new post with the `new` command (name your
post in kebab-case, eg `hello-world`).

```
$ cd <project_name>
$ aurora new <post_title>
```

A new markdown file under the `/posts` directory will be created. The filename
includes the current date and the post title, for example
`2019-04-29-hello-world.md`. The top of the file is a block of YAML
frontmatter, the metadata for your post.

Add some content to your post below the frontmatter. Aurora only supports
content written in the Markdown format for now.

```markdown
---
title: Hello world
---

*Oh, what a day… What a lovely day!* - Nux
```

Now we can add a blog index to the homepage. Open the `/pages/index.html` file
and add the following in-between the `{% block content %}` and
`{% endblock %}` tags.

```jinja
<h2>Posts</h2>

<ol>
{% for _, post in posts.items() %}
    <a href="{{ post.url }}"><li>{{ post.title }}</li></a>
{% endfor %}
</ol>
```

Aurora uses the Jinja templating engine for compile-time logic. The `{% ... %}`
tags expresses control flow while `{{ ... }}` are variables.

Finally, build your website with

```
$ aurora build
```

The generated output can be found under the newly created `/dist` directory.
You can deploy the site using any methods you prefer. For local development,
simply run

```
$ python3 -m http.server
```

and visit http://0.0.0.0:8000 to preview your work.
