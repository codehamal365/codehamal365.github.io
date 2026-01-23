# Chirpy Starter

[![Gem Version](https://img.shields.io/gem/v/jekyll-theme-chirpy)][gem]&nbsp;
[![GitHub license](https://img.shields.io/github/license/cotes2020/chirpy-starter.svg?color=blue)][mit]

When installing the [**Chirpy**][chirpy] theme through [RubyGems.org][gem], Jekyll can only read files in the folders
`_data`, `_layouts`, `_includes`, `_sass` and `assets`, as well as a small part of options of the `_config.yml` file
from the theme's gem. If you have ever installed this theme gem, you can use the command
`bundle info --path jekyll-theme-chirpy` to locate these files.

The Jekyll team claims that this is to leave the ball in the user’s court, but this also results in users not being
able to enjoy the out-of-the-box experience when using feature-rich themes.

To fully use all the features of **Chirpy**, you need to copy the other critical files from the theme's gem to your
Jekyll site. The following is a list of targets:

```shell
.
├── _config.yml
├── _plugins
├── _tabs
└── index.html
```

To save you time, and also in case you lose some files while copying, we extract those files/configurations of the
latest version of the **Chirpy** theme and the [CD][CD] workflow to here, so that you can start writing in minutes.

## Prerequisites

Follow the instructions in the [Jekyll Docs](https://jekyllrb.com/docs/installation/) to complete the installation of
the basic environment. [Git](https://git-scm.com/) also needs to be installed.

## Installation

Sign in to GitHub and [**use this template**][use-template] to generate a brand new repository and name it
`USERNAME.github.io`, where `USERNAME` represents your GitHub username.

Then clone it to your local machine and run:

```console
$ bundle
```

## Local Development Setup

### 1. Install Ruby Environment

This project requires Ruby 3.1 or higher. We recommend using a Ruby version manager for easy management.

**On macOS (using Homebrew and rbenv):**

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install rbenv and ruby-build
brew install rbenv ruby-build

# Add rbenv to your shell (add to ~/.zshrc)
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# Install Ruby 3.1.4 (or latest compatible version)
rbenv install 3.1.4
rbenv global 3.1.4

# Verify installation
ruby -v
```

**Alternative: Using asdf (cross-platform)**

```bash
# Install asdf
brew install asdf

# Add Ruby plugin
asdf plugin add ruby

# Install Ruby
asdf install ruby 3.1.4
asdf global ruby 3.1.4
```

### 2. Install Bundler

Bundler manages Ruby gem dependencies:

```bash
gem install bundler
```

### 3. Install Project Dependencies

Navigate to your project directory and install the required gems:

```bash
cd /path/to/your/codehamal365.github.io
bundle install
```

This will install Jekyll and the Chirpy theme along with all dependencies specified in the `Gemfile`.

### 4. Start the Local Development Server

Run the Jekyll development server:

```bash
bundle exec jekyll serve
```

**Common options:**
- `--host 0.0.0.0`: Bind to all interfaces (accessible from other devices on network)
- `--port 3000`: Use a different port (default is 4000)
- `--drafts`: Include draft posts in the build
- `--watch`: Watch for changes and rebuild automatically (enabled by default)

**Example with options:**
```bash
bundle exec jekyll serve --host 0.0.0.0 --port 4000 --drafts
```

The site will be available at `http://localhost:4000` (or your specified host/port).

### 5. Development Workflow

1. Make changes to your posts in the `_posts/` directory
2. The site will automatically rebuild when you save files
3. View changes in your browser at the local server URL
4. Commit and push changes to deploy to GitHub Pages

### Troubleshooting

**Ruby version issues:**
- Ensure rbenv/asdf is properly configured: `ruby -v` should show the correct version
- If using system Ruby, you may encounter permission issues

**Bundle install fails:**
- Update RubyGems: `gem update --system`
- Clear gem cache: `gem cleanup`

**Jekyll serve fails:**
- Check for missing dependencies: `bundle check`
- Reinstall dependencies: `bundle install --force`

**Port already in use:**
- Kill existing process: `lsof -ti:4000 | xargs kill -9`
- Or use a different port: `bundle exec jekyll serve --port 3000`

For more detailed troubleshooting, see the [Jekyll documentation](https://jekyllrb.com/docs/troubleshooting/) and [Chirpy theme issues](https://github.com/cotes2020/jekyll-theme-chirpy/issues).

## Usage

Please see the [theme's docs](https://github.com/cotes2020/jekyll-theme-chirpy#documentation).

## Contributing

The contents of this repository are automatically updated when new releases are made to the [main repository][chirpy].  
If you have problems using it, or would like to participate in improving it, please go to the main repository for feedback!

## License

This work is published under [MIT][mit] License.

[gem]: https://rubygems.org/gems/jekyll-theme-chirpy
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[use-template]: https://github.com/cotes2020/chirpy-starter/generate
[CD]: https://en.wikipedia.org/wiki/Continuous_deployment
[mit]: https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE
