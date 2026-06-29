# ulauncher-plocate-search

A [Ulauncher](https://ulauncher.io/) extension for fast file search using `plocate` — similar to macOS Spotlight.

## Features

- Fast file search powered by `plocate`
- Case-insensitive search
- Click a result to open the file directly
- Run `updatedb` to refresh the file index without leaving Ulauncher

## Requirements

### 1. Ulauncher (v5+)

**Arch Linux / Manjaro:**
```bash
sudo pacman -S ulauncher
```

**Ubuntu / Debian:**
```bash
sudo add-apt-repository universe
sudo apt update && sudo apt install ulauncher
```

**Fedora:**
```bash
sudo dnf install ulauncher
```

### 2. plocate

**Arch Linux / Manjaro:**
```bash
sudo pacman -S plocate
```

**Ubuntu / Debian:**
```bash
sudo apt install plocate
```

**Fedora:**
```bash
sudo dnf install plocate
```

### 3. Build the initial file index

```bash
sudo updatedb
```

> Note: Run `sudo updatedb` periodically to keep the index up to date. You can also trigger it from within the extension (see Usage).

### 4. Python dependencies

This extension uses only Python standard library modules. No extra `pip` packages needed.

## Installation

1. Open Ulauncher → **Preferences** → **Extensions** tab
2. Click **"Add extension"**
3. Paste the URL:
   ```
   https://github.com/hoanggminh2702/ulauncher-plocate-search
   ```
4. Click **Add**

## Usage

| Action | How |
|--------|-----|
| Search for a file | Type `f <filename>` in Ulauncher |
| Open a file | Click on a search result |
| Refresh file index | Type `f` (without query) → click **"Update plocate database"** |

> The default keyword is `f`. You can change it in Ulauncher → Preferences → Extensions → Plocate Fuzzy Search.

## Troubleshooting

**No results found:**
- Run `sudo updatedb` to build/refresh the index
- Make sure `plocate` is installed: `which plocate`
- Test manually: `plocate -i <filename>`

**Permission error when running updatedb:**
- `updatedb` requires root on some systems. Run `sudo updatedb` manually, or configure a sudoers rule:
  ```
  your_username ALL=(ALL) NOPASSWD: /usr/bin/updatedb
  ```

## License

MIT
