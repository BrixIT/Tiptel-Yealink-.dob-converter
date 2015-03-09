# Tiptel and Yealink image converter

This tool converts images to .dob files to use as logo in Tiptel and Yealink phones

## Dependencies

- python3
- pillow

## Usage

```bash
# Convert logo to .dob without resizing
$ ./convert.py logo.png logo.dob

# Convert logo to .dob for a Tiptel IP 286
$ ./convert.py -p ip286 logo.png logo.dob

# Convert .dob back to a .png
$ ./convert.py -r logo.dob logo.png
```