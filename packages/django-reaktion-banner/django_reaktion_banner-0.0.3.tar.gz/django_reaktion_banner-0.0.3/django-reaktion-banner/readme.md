## Banners app

### Backend configuration

> Add `BANNER_ENDPOINT` to env
```
BANNERS_ENDPOINT = os.environ['BANNERS_ENDPOINT']
```

> Install App
```
       INSTALLED_APPS = [
           ...,
           'banner',
           ...
       ]
```

> Set up Custom filters

In `TEMPLATES` add:
```
        'OPTIONS': {
            'context_processors': [
                ...
            ],
            'libraries' : {
                'custom_tags' : 'banner.templatetags.custom_tags'
            }
        }
```

> Set up Processors

In `TEMPLATES` add:
```
        'OPTIONS': {
            'context_processors': [
                ...
                'banner.processors.banner_endpoint',
                'banner.processors.banner_top',
                'banner.processors.banner_sidebar_right',
                'banner.processors.banner_sidebar_left',
                'banner.processors.banner_content',
                'banner.processors.banner_bottom',
            ]
```

> Migrate
```
./manage.py makemigrations
./manage.py migrate
```

> Tests
```
./manage.py test banner.test_api
```

### Frontend setup

> Add `banner.js` to your template and define API_ENDPOINT
```
<script defer type="text/javascript" src="{% static 'banner/banner.js' %}"></script>    
```

> Set up boxes where ads are visible.
```
<div class="... banner-box" banner-id="{{banner_top.id}" banner-url="{{banner_top.url}}">
    <img src="{{banner_top.image}}" />
</div>
```

> Available banners positions (TODO: banners sizes):
- `banner_top` 
- `banner_sidebar_right`
- `banner_sidebar_left`
- `banner_sidebar_content`
- `banner_content`
- `banner_bottom`

### Statistics / Numbers

- Download statistics for banner
- Download all click's statistic for banner

![actions](./img/actions.png)

- Impressions, view, clicks summaries are visible in banner's view

![stats](./img/stats.png)


