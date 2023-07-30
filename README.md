# neavey.net

[![Netlify Status](https://api.netlify.com/api/v1/badges/6bd28497-7039-4b4f-8090-9d2e591c6d64/deploy-status)](https://app.netlify.com/sites/neaveynet/deploys)

This site has been generated with [Hugo](https://gohugo.io) using the [LoveIt theme](https://github.com/dillonzq/LoveIt), and stored publicly here on Github. Updates are done on the go using a Git client, changes are then uploaded to Github and detected by [Netlify](https://www.netlify.com/) to trigger automatic deploys.

Anyone considering a similiar setup, check out the following articles:

[Hugo on the Go: Static Blogging from an iPhone](http://evanbrown.io/post/hugo-on-the-go/)

# Notes

Images larger than 700k optimized with _optipng_ or _jpegoptim_.

```
   $ fd -e jpeg -e jpg -S +700k -x jpegoptim --size=600k {}
```

```
   $ optipng <filename.png>
```

HEIC Conversion

```
   $ heif-convert -q 100 IMG_xxxx.heic IMG_xxxx.jpeg
   $ convert IMG_xxx.jpeg -resize 1024x1024 IMG_xxx.jpeg
```
