---
date: '{{ time.Now.Format "2006-01-02" }}'
categories:
  - Blog
# title defaults to the filename you used when creating the post
title: '{{ replace .File.ContentBaseName `-` ` ` | title }}'
author: # should match the key with your username in data/authors.yaml
# slug is not needed unless you want to change the url where this page is displayed
---

Usage:

```
❯ hugo new content blog/this-is-a-new-blogpost.md
Content "/Users/fzipitria/Workspace/OWASP/website/content/blog/this-is-a-new-blogpost.md" created
❯ cat "/Users/fzipitria/Workspace/OWASP/website/content/blog/this-is-a-new-blogpost.md"
---
date: '2024-06-04'
categories:
  - Blog
# title defaults to the filename you used when creating the post
title: 'This Is a New Blogpost'
author: # should match the key with your username in data/authors.yaml
# slug is not needed unless you want to change the url where this page is displayed
---

Usage:

```
hugo new content blog/this-is-a-new-blogpost.md
```%
```