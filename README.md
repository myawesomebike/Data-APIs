# Connect to popular APIs with Python

These modules connect to APIs for image processing, organic reporting, and popular forums including reddit and Stack Exchange.  Data from these APIs can be used for audience insights, image analysis, market research, and reporting.  Some APIs may require paid accounts with the sites or data providers.

(Please see [Google-APIs repo](https://github.com/myawesomebike/Google-APIs) for Google-specific APIs)

## Microsoft Azure Cognitive Services/Computer Vision API

This Python module can process a list of publically-accessible image URLs through Microsoft's Computer Vision API.  The Computer Vision API will return categories, tags, foreground, and background color for each submitted image for output to a CSV.  The image data can be processed against ad copy or target keywords, on-page copy, or to summarize image content automatically.

## Search reddit with a Tkinter GUI

The reddit module utilizes Tkinter to respond to user request, update progress, and export comments from subreddits.  The tool allows seaches of 5 subreddits for 5 keywords or topics (each separated by commas).  Comments from the matching subreddits containing the target keywords will be exported to a CSV.  Ngrams for each content will be generated (with matching comment ID) and exported to a seperate CSV.

## SEMrush Domain History

Get basic domain ranking metrics from SEMrush.  This module reads a list of domains and exports any postion-level data to a CSV.

## Stack Exchange API

Search Stack Exchange for questions matching a search keywords.  The API returns any questions that have been answered on Stack Exchange including their answers.  The questions and related answers are exported to a CSV.

## Stat API

Connect to the Stat API and request basic keyword and ranking data from an established account.
