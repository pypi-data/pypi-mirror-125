 image-filter
==============

[![PyPI version](https://badge.fury.io/py/lektor-image-filter.svg)](https://badge.fury.io/py/lektor-image-filter)
[![Downloads](https://pepy.tech/badge/lektor-image-filter)](https://pepy.tech/project/lektor-image-filter)
[![Linting Python package](https://github.com/chaos-bodensee/lektor-image-filter/actions/workflows/pythonpackage.yml/badge.svg)](https://github.com/chaos-bodensee/lektor-image-filter/actions/workflows/pythonpackage.yml)
[![Upload Python Package](https://github.com/chaos-bodensee/lektor-image-filter/actions/workflows/pythonpublish.yml/badge.svg)](https://github.com/chaos-bodensee/lektor-image-filter/actions/workflows/pythonpublish.yml)
[![MIT License](https://raw.githubusercontent.com/chaos-bodensee/lektor-image-filter/main/.github/license.svg?sanitize=true)](https://github.com/chaos-bodensee/lektor-image-filter/blob/main/LICENSE)

A [Lektor](https://getlektor.com) filter to print the input image in different predefined image sizes.

This plugin is designed to work together with the [lektor-image-resize](https://github.com/chaos-bodensee/lektor-image-resize) Plugin.

 Current Filters:
------------------
 + ``imagessrcsetwebp`` will print the configured sizes as ``webp`` to put in a ``srcset`` element.
 + ``imagessrcwebp`` will print the first configured ``webp`` image name to put in a ``src`` element.
 + ``imagessrcsetjpg`` will print the configured sizes as ``jpg`` to put in a ``srcset`` element.
 + ``imagessrcjpg`` will print the first configured ``jpg`` image name to put in a ``src`` element.
 + ``firstwidth`` will print the first configured  image width to put in a ``width`` element. If you use the [Advanced Lektor Example](#advanced-lektor-example) we try to compute the width if no is provided,
 + ``firstheight`` will print the first configured  image height to put in a ``height`` element. If you use the [Advanced Lektor Example](#advanced-lektor-example) we try to compute the height if no is provided,

 Configuration
---------------
You can configure the image width in the config file called `configs/image-resize.ini` and add
a few sections for images. The section names can be whatever you want, the
final images will be called ``$(imagename)-$(sectionname).jpg`` and ``$(imagename)-$(sectionname).webp``.

If the ``width`` enty does not exist the entry will be ignored.

Here is a example config file:

```ini
[small]
width = 640
height = 360

[medium]
height = 720

[woowee]
width = 1920
```

 Simple Lektor Example
----------------

### Lektor Jinja2 Input
```html
<img src="{{ 'waffle.jpg'|imagessrcjpg }}"
  width="{{ 'random_string'|firstwidth }}" height="{{ ''|firstheight }}"
  srcset="{{ 'waffle.jpg'|imagessrcsetjpg }}" />
```

### Lektor HTML Output:
```html
<img src="waffle-small.webp"
  width="640" height="360"
  srcset="waffle-small.webp  640w,
          waffle-woowee.webp 1280w,
          waffle-woowee.webp 1920w" />
```

-> If the ``width`` is not defined the option will be skipped in srcset!

 Advanced Lektor Example
-------------------------
### Lektor Models Definition
```ini
[fields.my_image]
label = Example Image
description = Select a Image from the Attatchments of this site. Upload one, if no one is available
type = select
source = record.attachments.images
```
### Lektor Jinja2 Input
```html
{% set image = record.attachments.images.get(this.my_image) %}
<img src="{{ image | imagessrcwebp }}"
     width="{{ image | firstwidth }}" height="{{ image | firstheight }}"
     srcset="{{ image | imagessrcsetwebp }}" />
```
#### Explaination Input:
- First we created the Jinaja2-variable ``image`` that will contain our image (``this.box_image``) to make this example better readable. *(We assume you know how to create variables in lektor)*
- Next line we created a html image tag with ``src`` and ``width``
- Last we created the ``srcset`` element with all configured sizes.

### Lektor HTML Output
```html
<img src="waffle-small.webp"
  width="640" height="360"
  srcset="waffle-small.webp  640w,
          waffle-medium.webp 1280w,
          waffle-woowee.webp 1920w" />
```
-> If the ``width`` is not defined we try to compute the option based on the ``height`` entry and the source image aspect ratio.

*(Please note that we added some new lines to make the example better readable and we assume that ``my_image: waffle.jpg`` comes from your .lr file, created via lektor admin menu)* and is a image in ``16:9`` aspect ratio.

 Installation
--------------
```bash
lektor plugin add lektor-image-filter
```