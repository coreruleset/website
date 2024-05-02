## Streamline Your Workflow: Writing for Core Ruleset with Hugo

Do you contribute content to the Core Ruleset (CRS) project and crave a more efficient way to create and manage blog posts? Look no further than Hugo, a static site generator, paired with the official CRS website hosted on [https://coreruleset.org/](https://coreruleset.org/). This combo offers a powerful alternative for streamlining your writing and publishing process.

This guide equips you, whether a seasoned writer or new contributor, with the essentials of crafting blog posts in Hugo for the CRS website. We'll cover adding images, cross-linking content, and including URLs – all familiar tasks you might be accustomed to from other platforms.

### Getting Started with Hugo

Hugo utilizes Markdown, a familiar syntax for writing content, making the transition smooth. Here's a quick setup guide:

1. **Install Hugo:** Download and install Hugo from the official website [https://gohugo.io/](https://gohugo.io/).
2. **Clone the Core Ruleset Website Repository:** Head over to GitHub and clone the official CRS website repository: [https://github.com/coreruleset/website](https://github.com/coreruleset/website). Don't forget to do the clone recursive!
3. **Start the Server (Optional):** Navigate to the cloned repository directory and run `hugo server` to launch a local development server, allowing you to preview your changes at `http://localhost:1313` by default. This step is optional for previewing purposes, but not required for contributing content.

### Crafting Your Blog Post

The CRS website leverages Hugo for content management. Here's how to create a new blog post:

1. **Content Folder:** Locate the `content/blog` directory within the cloned repository. This is where you'll create your new Markdown file.
2. **Create a New File:** Use your preferred text editor to create a new Markdown file with a descriptive filename (e.g., `my-new-post.md`).
3. **Front Matter:** At the beginning of your Markdown file, include a section called "front matter." This section uses YAML syntax to define metadata about your blog post. Here are the essential fields:
    * **title:** (Required) A descriptive title for your blog post.
    * **date:** (Required) The publication date in YYYY-MM-DD format.
    * **tags:** (Optional) A comma-separated list of keywords or categories relevant to your post.

Here's an example of a basic front matter section:

```yaml
---
title: My Exciting Blog Post about CRS
date: 2024-04-16
tags: core-ruleset, security
---
```

4. **Write Your Content:** Now that you've defined the metadata, proceed with composing your blog post using Markdown syntax. Hugo offers a comprehensive reference for guidance: https://gohugo.io/content-management/organization/.

### Enhancing Your Post with Visuals

Adding visuals to your blog post is a breeze with Hugo. Here's how:

1. **Upload Images:** Place your images in a folder named "static" within the project directory. Let's assume your image is named "myimage.jpg".
2. **Use the `figure` shortcode:** In your Markdown blog post file, embed the image using the shortcode:

```markdown
{{< figure src="/static/myimage.jpg" alt="My Image Description" >}}
```

* Replace `/static/myimage.jpg` with the relative path to your image.
* Add a descriptive `alt` text attribute for accessibility.

**Pro-Tip:** Organize your images within subfolders inside "static" for better project management. Just update the path in the shortcode accordingly (e.g., `/static/images/myimage.jpg`).

### Cross-linking Your Content

Similar to other platforms, Hugo allows you to link between blog posts for a seamless reading experience within the CRS website. Here's how:

1. **Use relative URLs:** When mentioning another post, use its filename within the content folder. For example, to link to a post named "another-post.md":

```markdown
You can read more about it in my previous post [here]({{< ref "another-post.md" >}}).
```

* Hugo automatically generates the correct link when you build the site. You don't need to know the title of the post, or anything else than the path of the file, relative to the `content/` directory.

2. **Advanced Linking:**  For more complex scenarios, Hugo offers features like shortcodes for named links and taxonomies for categorizing posts. Refer to the official documentation for details: [https://gohugo.io/content-management/shortcodes/](https://gohugo.io/content-management/shortcodes/)

### Including External URLs

Adding hyperlinks to external websites is straightforward:

```markdown
Visit the official Hugo website [here](https://gohugo.io).
```

Simply enclose the URL in brackets after your desired link text.

### Sharing Your Work: The Pull Request Process

Once you're happy with your crafted blog post, it's time to contribute it to the CRS website! Here's how to submit your changes via a pull request:

1. **Commit Your Changes:** In your terminal, navigate to the cloned repository directory and stage your changes using `git add <filename>`. You can also use `git add .` to stage all modified files. Then, commit your changes with a descriptive message using `git commit -m "My blog post contribution: [Post Title]"`.
2. **Push to Your Fork:** Assuming you've forked the CRS website repository on GitHub, push your local commits to your fork and then create a new Pull Request to the coreruleset website repo. That's it!
