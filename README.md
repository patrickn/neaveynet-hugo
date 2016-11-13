# neavey.net

![](https://travis-ci.org/patrickn/neaveynet-hugo.svg?branch=master)

This site has been generated with [Hugo](https://gohugo.io) using the [Icarus theme](https://github.com/digitalcraftsman/hugo-icarus-theme), and stored publicly here on Github. Updates are done on the go using a Git client, changes are then uploaded to Github where a [Travis CI](https://travis-ci.org/) job generates the site and deploys to Amazon S3.

The S3 site is behind Amazons CloudFront CDN, which enables the use of https.

Anyone considering a similiar setup, check out the following articles:

[Hugo on the Go: Static Blogging from an iPhone](http://evanbrown.io/post/hugo-on-the-go/)

[Let's Encrypt a Static Site on Amazon S3](https://www.codeword.xyz/2016/01/06/lets-encrypt-a-static-site-on-amazon-s3/)

[Host a Static Site on AWS, using S3 and CloudFront](https://www.davidbaumgold.com/tutorials/host-static-site-aws-s3-cloudfront/)