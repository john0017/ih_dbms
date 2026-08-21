# IH DBMS

A Flask-based property management prototype for reviewing and maintaining residential property acquisition records stored in MySQL.

## Overview

IH DBMS provides a browser-based interface for working with property portfolio data. It combines a Flask web application with Pandas-based data processing and a MySQL database, allowing users to view, filter, add, update, and remove property records.

The repository also contains exploratory work for matching property addresses against Ireland's Property Price Register using fuzzy text matching and sale-date proximity.

## Features

- Session-protected application views
- Property portfolio table and record detail pages
- Filtering by acquisition status
- Add, update, and delete operations backed by MySQL
- UUID-based record identifiers
- Pandas-based database querying and presentation
- Fuzzy address matching against property transaction data
- Bootstrap-powered HTML interface

## Technology

- Python
- Flask
- MySQL
- Pandas
- Flask-Bootstrap
- Flask-WTF and WTForms
- FuzzyWuzzy
- Jupyter Notebook
- HTML templates

## Architecture

```text
Browser
   |
   v
Flask routes and session checks
   |
   +--> HTML templates
   |
   +--> Pandas data processing
   |
   v
MySQL property database
```

## Project Status

This repository represents an early prototype and learning project. It is not configured for production deployment.

## Security Notice

Review the repository's configuration and sample data before running or sharing the application. Database credentials and application secrets should be supplied through environment variables or a secure secrets manager, never committed to source control.

## Potential Improvements

- Move configuration and credentials to environment variables
- Add password verification and secure user management
- Introduce database migrations and an ORM
- Add automated tests and input validation
- Separate development, testing, and production configuration
- Add containerized local setup
