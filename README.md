# rest_api
A sample REST API to deal with waste streams


# Project Name

Seenons REST API

## Description
A sample REST API to deal with waste streams.

## Installation

# Clone the repository
git clone <repository-url>

# Navigate to the project directory
cd <project-directory>

# Install dependencies
pip install -r requirements.txt

# Build and install project
make

# Run project
make run (or run_seenons_api)

## Usage

# Endpoint
The API is available at the /streams/ endpoint.

# Basic request with mandatory postcode
curl -X 'GET' 'http://localhost:5000/streams/?postalcode=1500SS'

# Request with optional weekdays parameter
curl -X 'GET' 'http://localhost:5000/streams/?postalcode=1500SS&weekdays[]=monday&weekdays[]=tuesday'

